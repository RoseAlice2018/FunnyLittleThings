#include <iostream>
#include <ftw.h>
#include <fstream>
#include <cerrno>
#include <ctime>
#include <dirent.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string>
#include <mysql.h>
#include <nlohmann/json.hpp>
#include <set>
#include <regex>
using json = nlohmann::json;

// 数据库配置
json configJson;

struct DBConfig{
    std::string dbname;
    std::string dbtable;
    std::string user;
    std::string password;
};

struct FilePathConfig{
    std::string filepath;
};

struct SkipFileConfig{
    std::set<std::string> skipDirectories;
    std::set<std::string> skipFiles;
};


static DBConfig db_config;
static FilePathConfig file_config;
static SkipFileConfig skip_config;

std::string trim(const std::string& str) {
    const std::regex trimRegex("^\\s+|\\s+$");
    return std::regex_replace(str, trimRegex, "");
}

int _init_config()
{
    std::ifstream configFile("./config/config.json");
    if(configFile.is_open())
    {
        configFile >> configJson;
        configFile.close();   
        // db
        db_config.dbname = configJson["database"]["dbname"];
        db_config.dbtable = configJson["database"]["table"];
        db_config.user = configJson["database"]["user"];
        db_config.password = configJson["database"]["password"];
        // file
        file_config.filepath = configJson["filepath"]["mainpath"];
        //skip
        std::string skipDirectories = configJson["skippath"]["skipdirectories"];
        std::string skipFiles = configJson["skippath"]["skipfile"];

        std::istringstream dirStream(skipDirectories);
        std::string dirName;
        while(std::getline(dirStream, dirName, ',')){
            skip_config.skipDirectories.insert(trim(dirName));
            std::cout<<"dirname:"<<trim(dirName)<<std::endl;
        }
        std::istringstream filestream(skipFiles);
        std::string filename;
        while(std::getline(filestream, filename, ',')){
            skip_config.skipFiles.insert(trim(filename));
            std::cout<<"filename:"<<trim(filename)<<std::endl;
        }
    }

    return 0;
}

int init()
{
    int ret = 0;
    // init config
    ret =  _init_config();
    if(ret != 0)
    {
        // error log
        return ret;
    }
    return ret;
}


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
                            const std::string& date, const std::string& bytes){
            if(conn == NULL){
                std::cerr<<"Database connection is not initialized."<<std::endl;
                return false;
            }
            std::string query = "INSERT INTO " + table + " (file_name, record_date, file_size) VALUES ('" + filename 
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
    for (const auto& dir : skip_config.skipDirectories) {
        std::cout << "Skip directory: " << dir << std::endl;
    }
    // skip
    std::string basepath = fpath;
    size_t pos = basepath.find_last_of("/\\");
    if (pos != std::string::npos) {
        basepath = basepath.substr(0, pos);
    }

    std::string basename = fpath;
    size_t last_oeprator = basename.find_last_of("/\\");
    if (last_oeprator != std::string::npos){
        basename = basename.substr(last_oeprator + 1);
    }

    std::cout<<"fpath："<<basepath<<std::endl<<"basename "<<basename<<std::endl;
    // 检查是否是目录且需要跳过
    if (skip_config.skipDirectories.find(basepath) != skip_config.skipDirectories.end()) {
        std::cout<<"Hi Skip Here"<<fpath<<" "<<basename<<std::endl;
        return FTW_SKIP_SUBTREE; // 跳过当前目录及其子目录
    }
    std::cout<<"we don't skip fpath："<<basepath<<std::endl<<"basename "<<basename<<std::endl;
    // 检查是否是文件且需要跳过
    if (typeflag == FTW_F && skip_config.skipFiles.find(basename) != skip_config.skipFiles.end()) {
        std::cout<<"we  skip fpath："<<basepath<<std::endl<<"basename "<<basename<<std::endl;
        return 0; // 跳过当前文件
    }

    MYSQL *conn = DatabaseConnection::getInstance("localhost", db_config.user.c_str(), db_config.password.c_str(), db_config.dbname.c_str())->getConnection();
    if(conn == NULL){
        std::cerr<<"DatabaseConnection is not initialized"<<std::endl;
        return -1;
    }

    // 检查是否是普通文件
    if (typeflag == FTW_F){
        std::cout<<"we have fpath："<<basepath<<std::endl<<"basename "<<basename<<std::endl;
        std::string filename = std::string(fpath);
        std::ofstream outfile;
        std::string date_str = getCurrentDate();
        std::string dir_path = "./data";
        ensureDirExists(dir_path);

        //这里主要是不操作数据库，而通过txt存储数据。
        //std::string filepath = dir_path + "/" + date_str + ".txt";

        //outfile.open(filepath.c_str(), std::ios_base::app);
        // if(!outfile.is_open()){
        //     std::cerr << "Error opening file: " << filepath << std::endl;
        //     return -1;
        // }
        // outfile << "当前计算文件路径名:" << filename << " 字节数:" << sb->st_size << std::endl;
        //std::cout<<filepath<<std::endl;
        //outfile.close();

        DatabaseConnection *dbconn = DatabaseConnection::getInstance("localhost", db_config.user.c_str(), db_config.password.c_str(), db_config.dbname.c_str());
        std::string bytes = std::to_string((int)sb->st_size);
        if(!dbconn->insertData("WORDSCAL", filename, date_str, bytes)){
            std::cerr<<"Failed to insert data into the database." <<std::endl;
            return -1;
        }
    }
    return 0;
}

void TestMySQLConnection()
{
    MYSQL *conn = DatabaseConnection::getInstance("localhost", db_config.user.c_str(), db_config.password.c_str(), db_config.dbname.c_str())->getConnection();
    if(conn == NULL){
        std::cerr<<"DatabaseConnection is not initialized"<<std::endl;
        return;
    }
    std::cerr<<"DatabaseConnection is OK"<<std::endl;
}

int main(){
    int flags = FTW_PHYS;   // 使用物理路径，不跟随符号链接

    int ret = 0;

    ret = init();
    if(ret != 0)
    {
        // error log
        return ret;
    }

    //TestMySQLConnection();
    //使用nftw递归遍历目录
    if(nftw(file_config.filepath.c_str(), fileCallback, 1000, flags) == -1){
        std::cerr<<"Error occurred during directory traversal"<<std::endl;
        return 1;
    }
    return 0;
}