package com.habitbloom.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.habitbloom.data.database.entity.HabitRecord;

import java.util.List;

@Dao
public interface HabitRecordDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(HabitRecord record);

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<HabitRecord> records);

    @Update
    void update(HabitRecord record);

    @Delete
    void delete(HabitRecord record);

    @Query("SELECT * FROM habit_records WHERE record_id = :recordId")
    LiveData<HabitRecord> getRecordById(long recordId);

    @Query("SELECT * FROM habit_records WHERE habit_id = :habitId AND record_date = :date")
    HabitRecord getRecordByHabitAndDate(long habitId, String date);

    @Query("SELECT * FROM habit_records WHERE habit_id = :habitId ORDER BY record_date DESC")
    LiveData<List<HabitRecord>> getRecordsByHabit(long habitId);

    @Query("SELECT * FROM habit_records WHERE habit_id = :habitId ORDER BY record_date DESC")
    List<HabitRecord> getRecordsByHabitSync(long habitId);

    @Query("SELECT * FROM habit_records WHERE habit_id = :habitId AND record_date BETWEEN :startDate AND :endDate ORDER BY record_date")
    List<HabitRecord> getRecordsByHabitInRange(long habitId, String startDate, String endDate);

    @Query("SELECT * FROM habit_records WHERE habit_id = :habitId AND completed = 1 ORDER BY record_date DESC")
    List<HabitRecord> getCompletedRecordsByHabit(long habitId);

    @Query("SELECT COUNT(*) FROM habit_records WHERE habit_id = :habitId AND completed = 1")
    int getCompletedCount(long habitId);

    @Query("SELECT COUNT(*) FROM habit_records WHERE habit_id = :habitId AND completed = 1 AND record_date BETWEEN :startDate AND :endDate")
    int getCompletedCountInRange(long habitId, String startDate, String endDate);

    @Query("SELECT * FROM habit_records WHERE record_date = :date")
    List<HabitRecord> getRecordsByDate(String date);

    @Query("SELECT COUNT(*) FROM habit_records WHERE record_date = :date AND completed = 1")
    int getCompletedCountByDate(String date);

    @Query("DELETE FROM habit_records WHERE habit_id = :habitId")
    void deleteByHabitId(long habitId);

    /**
     * 获取习惯从某日期开始的连续打卡天数
     */
    @Query("SELECT COUNT(*) FROM habit_records WHERE habit_id = :habitId AND completed = 1 AND record_date <= :date ORDER BY record_date DESC")
    int getStreakEndingAt(long habitId, String date);

    /**
     * 检查今天是否已打卡
     */
    @Query("SELECT EXISTS(SELECT 1 FROM habit_records WHERE habit_id = :habitId AND record_date = :date AND completed = 1)")
    boolean isCompletedToday(long habitId, String date);
}
