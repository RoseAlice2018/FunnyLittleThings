#ifndef __WORDS_CAL_MANAGER_H__
#define __WORDS_CAL_MANAGER_H__

#include <string>

class cal_manager
{
private:
    /* data */
    std::string data_file_path;  // 数据描述路径
    
public:
    cal_manager(/* args */);
    void init(); 
    void daily_cal();
    void weekly_cal();
    void monthly_cal();
    void yearly_cal();
    ~cal_manager();
};

cal_manager::cal_manager(/* args */)
{
}

cal_manager::~cal_manager()
{
}


#endif