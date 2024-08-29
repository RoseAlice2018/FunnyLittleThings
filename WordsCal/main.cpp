#include <iostream>
#include <ftw.h>
#include <cstring>
#include <fstream>
#include <cerrno>
#include <ctime>
#include <dirent.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <mysql.h>


class DatabaseConnection{
    private:
        static DatabaseConnection *instance;
        MYSQL *conn;

        // 私有构造函数
        DatabaseConnection(const char *hostname, const char *username, const char *password, const char *database){
            conn = mysql_init(NULL);
            if(conn == NULL){
                std::cerr<<"mysql_init() failed\n";
            }else if(mysql_real_connect(conn, hostname, username, password, database, 0, NULL, 0) == NULL){
                std::cerr<<"mysql_real_connect() failed: "<<mysql_error(conn)<<std::endl;
                mysql_close(conn);
                conn = NULL;
            }
        }
        // 防止复制和赋值
        DatabaseConnection(const DatabaseConnection&) = delete;
        DatabaseConnection& operator=(const DatabaseConnection&) = delete;

    public:
        // 获取单例对象的静态方法
        static DatabaseConnection *getInstance(const char *hostname, const char *username, const char *password, const char *database){
            if(instance == NULL){
                instance = new DatabaseConnection(hostname, username, password, database);
            }
            return instance;
        }

        // 释放单例对象
        static void release(){
            if(instance){
                mysql_close(instance->conn);
                delete instance;
                instance = NULL;
            }
        }

        // 获取MYSQL指针
        MYSQL *getConnection(){
            return conn;
        }

        // 加入数据的方法
        bool insertData(const std::string& table, const std::string& filename,
                            const std::string& date, const std::string bytes){
            if(conn == NULL){
                std::cerr<<"Database connection is not initialized."<<std::endl;
                return false;
            }
            std::string query = "INSERT INTO" + table + "(FileID, Date, ByteCount) VALUES ('" + filename 
                        + "','" + date + "','" + bytes + "')";
            if(mysql_query(conn, query.c_str())){
                std::cerr<<"mysql_query() failed: "<<mysql_error(conn)<<std::endl;
                return false;
            } 
            return true;
        }

        // 析构函数
        ~DatabaseConnection(){
            if(conn){
                mysql_close(conn);
            }
        }
};

// 静态初始化成员变量
DatabaseConnection *DatabaseConnection::instance = NULL;

// 创建目录如果它不存在
void ensureDirExists(const std::string& dir)
{
    struct stat st = {0};
    if(stat(dir.c_str(), &st) == -1)
    {
        int res = mkdir(dir.c_str(), 0777);
        if(res != 0 && errno != EEXIST){
            std::cerr<<"Failed to create directory: "<< dir << std::endl;
            // exit(1);
        }
    }
}

// 获取当前日期格式化为YYYYMMDD
std::string getCurrentDate(){
    time_t now = time(NULL);
    struct tm tstruct;
    char buf[11];
    localtime_r(&now, &tstruct);
    strftime(buf, sizeof(buf), "%Y-%m-%d", &tstruct);
    return std::string(buf);
}


// 回调函数，用于处理每个文件或目录
int fileCallback(const char *fpath, const struct stat *sb, int typeflag, struct FTW *ftwbuf)
{
    MYSQL *conn = DatabaseConnection::getInstance("host", "user", "password", "database")->getConnection();
    if(conn == NULL){
        std::cerr<<"DatabaseConnection is not initialized"<<std::endl;
        return -1;
    }

    // 检查是否是普通文件
    if (typeflag == FTW_F){
        std::string filename = std::string(fpath);
        std::ofstream outfile;
        std::string date_str = getCurrentDate();
        std::string dir_path = "./data";
        ensureDirExists(dir_path);

        std::string filepath = dir_path + "/" + date_str + ".txt";

        outfile.open(filepath.c_str(), std::ios_base::app);
        if(!outfile.is_open()){
            std::cerr << "Error opening file: " << filepath << std::endl;
            return -1;
        }
        outfile << "当前计算文件路径名:" << filename << " 字节数:" << sb->st_size << std::endl;
        std::cout<<filepath<<std::endl;
        outfile.close();

        DatabaseConnection *dbconn = DatabaseConnection::getInstance("localhost", "user", "password", "database");
        if(!dbconn->insertData("Tablename", filename, date_str, std::to_string(sb->st_size))){
            std::cerr<<"Failed to insert data into the database." <<std::endl;
            return -1;
        }
    }
    return 0;
}

int main(){
    const char *path = "."; // 从当前目录开始遍历
    int flags = FTW_PHYS;   // 使用物理路径，不跟随符号链接

    // MySQL配置
    const char *hostname = "";
    const char *username = "";
    const char *password = "";
    const char *database = "";
    
    // MySQL数据库连接
    MYSQL *conn = mysql_init(NULL);
    if (conn == NULL){
        std::cerr<<"mysql_init() failed\n";
        return 1;
    }

    if(mysql_real_connect(conn, hostname, username, password, database, 0, NULL, 0) == NULL)
    {
        std::cerr<<"mysql_real_connect() failed: "<<mysql_error(conn)<<std::endl;
        mysql_close(conn);
        return 1;
    }

    // 使用nftw递归遍历目录
    if(nftw(path, fileCallback, 20, flags) == -1){
        std::cerr<<"Error occurred during directory traversal"<<std::endl;
        return 1;
    }
    return 0;
}