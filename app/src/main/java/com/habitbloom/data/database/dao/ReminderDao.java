package com.habitbloom.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.habitbloom.data.database.entity.Reminder;

import java.util.List;

@Dao
public interface ReminderDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(Reminder reminder);

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<Reminder> reminders);

    @Update
    void update(Reminder reminder);

    @Delete
    void delete(Reminder reminder);

    @Query("SELECT * FROM reminders WHERE reminder_id = :reminderId")
    LiveData<Reminder> getReminderById(long reminderId);

    @Query("SELECT * FROM reminders WHERE reminder_id = :reminderId")
    Reminder getReminderByIdSync(long reminderId);

    @Query("SELECT * FROM reminders WHERE habit_id = :habitId")
    LiveData<List<Reminder>> getRemindersByHabit(long habitId);

    @Query("SELECT * FROM reminders WHERE habit_id = :habitId")
    List<Reminder> getRemindersByHabitSync(long habitId);

    @Query("SELECT * FROM reminders WHERE is_active = 1")
    List<Reminder> getAllActiveReminders();

    @Query("SELECT * FROM reminders WHERE habit_id = :habitId AND is_active = 1")
    List<Reminder> getActiveRemindersByHabit(long habitId);

    @Query("UPDATE reminders SET is_active = :isActive WHERE reminder_id = :reminderId")
    void setActive(long reminderId, boolean isActive);

    @Query("DELETE FROM reminders WHERE habit_id = :habitId")
    void deleteByHabitId(long habitId);
}
