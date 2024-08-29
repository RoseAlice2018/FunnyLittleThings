#include "cal_manager.h"
#include <fstream>
#include <vector>
#include <iostream>

std::string getCurrentDate(){
    time_t now = time(NULL);
    struct tm tstruct;
    char buf[11];
    localtime_r(&now, &tstruct);
    strftime(buf, sizeof(buf), "%Y%m%d", &tstruct);
    return std::string(buf);
}

std::string getYesterDayDate()
{
    time_t now = time(NULL);
    struct tm tstruct;
    char buf[11];

    localtime_r(&now, &tstruct);

    tstruct.tm_mday -= 1;

    time_t yesterday = mktime(&tstruct);

    localtime_r(&yesterday, &tstruct);

    strftime(buf, sizeof(buf), "%Y%m%d", &tstruct);

    return std::string(buf);
}

std::vector<std::string> read_file_lines(const std::string& filepath){
    std::ifstream file(filepath);
    std::vector<std::string> lines;
    std::string line;

    if(!file.is_open()){
        std::cout<<"Could not open file: " + filepath;
    }

    while(std::getline(file, line)){
        //读出每行内容
    }

    file.close(); // 关闭文件
    return lines;
}

void cal_manager::daily_cal()
{
    std::string data_str = getCurrentDate();
    std::string yesterday_str = getYesterDayDate();
    //cur_data file
    std::string cur_date_file_path = data_file_path + "/" + data_str + ".txt";
    //yesterday file 
    std::string yesterday_file_path = data_file_path + "/" + yesterday_str + ".txt";
    
    //compare and cal
    //每日的增量写入新文件？
}


void cal_manager::monthly_cal()
{

}

void cal_manager::weekly_cal()
{

}

void cal_manager::init()
{
    // read file_path from config
}
