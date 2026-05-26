#!/usr/bin/env python3
"""
生成带有正确日期信息的FIT文件
"""

import sys
import os
from fit_tool.fit_file import FitFile
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.record_message import RecordMessage
from fit_tool.profile.messages.session_message import SessionMessage
from fit_tool.profile.messages.lap_message import LapMessage
from fit_tool.profile.messages.activity_message import ActivityMessage
from fit_tool.profile.profile_type import Sport, SubSport
from datetime import datetime, timezone, timedelta


def generate_fit(user_id, date, start_time, duration):
    """
    生成带有正确日期信息的FIT文件
    
    Args:
        user_id: 个人编号
        date: 日期，格式为YYYYMMDD
        start_time: 开始时间，格式为HHMM
        duration: 运动总时长，格式为MMSS
    """
    try:
        # 解析输入参数
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        hour = int(start_time[:2])
        minute = int(start_time[2:4])
        duration_min = int(duration[:2])
        duration_sec = int(duration[2:4])
        total_duration = duration_min * 60 + duration_sec
        
        # 生成随机距离：3 + (随机两位数 < 30) * 0.01 km
        import random
        random_distance = 3 + (random.randint(0, 29) * 0.01)
        total_distance = random_distance * 1000  # 转换为米
        
        # 计算开始时间（北京时间）
        beijing_time = datetime(year, month, day, hour, minute, 0)
        # 直接使用北京时间作为UTC时间，这样应用显示时会正确显示为北京时间
        start_timestamp = int(beijing_time.timestamp() * 1000)
        
        # 加载1.fit文件作为模板
        input_path = '1.fit'
        if not os.path.exists(input_path):
            print(f"错误: {input_path} 文件不存在")
            return False
        
        # 读取模板文件
        template_file = FitFile.from_file(input_path)
        
        # 提取轨迹点
        record_messages = []
        for record in template_file.records:
            if hasattr(record.message, 'timestamp') and hasattr(record.message, 'position_lat') and hasattr(record.message, 'position_long'):
                if record.message.position_lat is not None and record.message.position_long is not None:
                    record_messages.append({
                        'position_lat': record.message.position_lat,
                        'position_long': record.message.position_long
                    })
        
        # 创建新的FIT文件
        builder = FitFileBuilder()
        
        # 重新计算轨迹点时间
        for i, msg in enumerate(record_messages):
            # 计算相对位置
            relative_pos = i / len(record_messages) if len(record_messages) > 0 else 0
            # 计算新的时间戳
            new_timestamp = start_timestamp + int(relative_pos * total_duration * 1000)
            
            # 创建新的RecordMessage
            record = RecordMessage()
            record.timestamp = new_timestamp
            record.position_lat = msg['position_lat']
            record.position_long = msg['position_long']
            record.distance = total_distance * relative_pos
            
            builder.add(record)
        
        # 创建LapMessage
        LAP_DISTANCE = 400.0
        total_laps = max(1, int(total_distance / LAP_DISTANCE))
        
        for lap_num in range(total_laps):
            lap_start = start_timestamp + int(lap_num * (total_duration / total_laps) * 1000)
            lap_end = start_timestamp + int((lap_num + 1) * (total_duration / total_laps) * 1000)
            
            lap_msg = LapMessage()
            lap_msg.timestamp = lap_end
            lap_msg.start_time = lap_start
            lap_msg.total_elapsed_time = total_duration / total_laps
            lap_msg.total_distance = LAP_DISTANCE
            lap_msg.sport = Sport.RUNNING
            lap_msg.sub_sport = SubSport.GENERIC
            
            builder.add(lap_msg)
        
        # 创建SessionMessage
        session_msg = SessionMessage()
        session_msg.timestamp = start_timestamp + total_duration * 1000
        session_msg.start_time = start_timestamp
        session_msg.total_elapsed_time = total_duration
        session_msg.total_distance = total_distance
        session_msg.sport = Sport.RUNNING
        session_msg.sub_sport = SubSport.GENERIC
        session_msg.num_laps = total_laps
        session_msg.total_calories = int(total_distance / 1000 * 70)  # 每公里70卡路里
        session_msg.avg_running_cadence = 170  # 平均步频
        session_msg.avg_power = 250  # 平均功率
        session_msg.avg_stance_time = 230  # 平均触地时间
        
        builder.add(session_msg)
        
        # 创建ActivityMessage
        activity_msg = ActivityMessage()
        activity_msg.timestamp = start_timestamp + total_duration * 1000
        activity_msg.total_timer_time = total_duration
        activity_msg.num_sessions = 1
        activity_msg.type = 0  # Manual
        
        builder.add(activity_msg)
        
        # 构建并保存文件
        fit_file = builder.build()
        output_path = f'{user_id}.fit'
        fit_file.to_file(output_path)
        
        print(f"成功生成文件: {output_path}")
        return True
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("用法: python generate_fit.py <个人编号> <日期> <开始时间> <运动总时长>")
        print("示例: python generate_fit.py 021 20260414 1315 2103")
        sys.exit(1)
    
    user_id = sys.argv[1]
    date = sys.argv[2]
    start_time = sys.argv[3]
    duration = sys.argv[4]
    
    generate_fit(user_id, date, start_time, duration)
