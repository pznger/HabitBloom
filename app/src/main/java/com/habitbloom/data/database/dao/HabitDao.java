package com.habitbloom.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.habitbloom.data.database.entity.Habit;

import java.util.List;

@Dao
public interface HabitDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Habit habit);

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<Habit> habits);

    @Update
    void update(Habit habit);

    @Delete
    void delete(Habit habit);

    @Query("SELECT * FROM habits WHERE habit_id = :habitId")
    LiveData<Habit> getHabitById(long habitId);

    @Query("SELECT * FROM habits WHERE habit_id = :habitId")
    Habit getHabitByIdSync(long habitId);

    @Query("SELECT * FROM habits WHERE user_id = :userId AND is_active = 1 ORDER BY created_at DESC")
    LiveData<List<Habit>> getActiveHabitsByUser(long userId);

    @Query("SELECT * FROM habits WHERE user_id = :userId AND is_active = 1 ORDER BY created_at DESC")
    List<Habit> getActiveHabitsByUserSync(long userId);

    @Query("SELECT * FROM habits WHERE user_id = :userId ORDER BY created_at DESC")
    LiveData<List<Habit>> getAllHabitsByUser(long userId);

    @Query("SELECT * FROM habits WHERE user_id = :userId ORDER BY created_at DESC")
    List<Habit> getAllHabitsByUserSync(long userId);

    @Query("SELECT * FROM habits WHERE category = :category AND is_active = 1 ORDER BY created_at DESC")
    LiveData<List<Habit>> getHabitsByCategory(String category);

    @Query("UPDATE habits SET current_streak = :streak, longest_streak = CASE WHEN :streak > longest_streak THEN :streak ELSE longest_streak END WHERE habit_id = :habitId")
    void updateStreak(long habitId, int streak);

    @Query("UPDATE habits SET total_completed = total_completed + 1 WHERE habit_id = :habitId")
    void incrementTotalCompleted(long habitId);

    @Query("UPDATE habits SET is_active = :isActive WHERE habit_id = :habitId")
    void setActive(long habitId, boolean isActive);

    @Query("SELECT COUNT(*) FROM habits WHERE user_id = :userId AND is_active = 1")
    int getActiveHabitCount(long userId);

    @Query("SELECT MAX(longest_streak) FROM habits WHERE user_id = :userId")
    int getMaxLongestStreak(long userId);

    @Query("SELECT SUM(total_completed) FROM habits WHERE user_id = :userId")
    int getTotalCompletedCount(long userId);
}
