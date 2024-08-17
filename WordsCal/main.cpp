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
    strftime(buf, sizeof(buf), "%Y%m%d", &tstruct);
    return std::string(buf);
}


// 回调函数，用于处理每个文件或目录
int fileCallback(const char *fpath, const struct stat *sb, int typeflag, struct FTW *ftwbuf)
{
    // 检查是否是普通文件
    if (typeflag == FTW_F){
        std::string filename = std::string(fpath);
        std::ofstream outfile;
        std::string date_str = getCurrentDate();
        std::string dir_path = "./data";
        ensureDirExists(dir_path);

        std::string filepath = dir_path + "/" + date_str + ".txt";

        outfile.open(filepath, std::ios_base::app);
        if(!outfile.is_open()){
            std::cerr << "Error opening file: " << filepath << std::endl;
            return -1;
        }
        outfile << "当前计算文件路径名:" << filename << " 字节数:" << sb->st_size << std::endl;
        outfile.close();
    }
    return 0;
}

int main(){
    const char *path = "."; // 从当前目录开始遍历
    int flags = FTW_PHYS;   // 使用物理路径，不跟随符号链接

    // 使用nftw递归遍历目录
    if(nftw(path, fileCallback, 20, flags) == -1){
        std::cerr<<"Error occurred during directory traversal"<<std::endl;
        return 1;
    }
    return 0;
}