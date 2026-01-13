package com.habitbloom.data.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "reminders",
        foreignKeys = @ForeignKey(
                entity = Habit.class,
                parentColumns = "habit_id",
                childColumns = "habit_id",
                onDelete = ForeignKey.CASCADE
        ),
        indices = {@Index("habit_id")})
public class Reminder {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "reminder_id")
    private long reminderId;

    @ColumnInfo(name = "habit_id")
    private long habitId;

    @ColumnInfo(name = "reminder_time")
    private String reminderTime; // HH:mm

    @ColumnInfo(name = "days_of_week")
    private String daysOfWeek = "1,2,3,4,5,6,7"; // 1=周日,2=周一...7=周六

    @ColumnInfo(name = "is_active")
    private boolean isActive = true;

    // Getters and Setters
    public long getReminderId() {
        return reminderId;
    }

    public void setReminderId(long reminderId) {
        this.reminderId = reminderId;
    }

    public long getHabitId() {
        return habitId;
    }

    public void setHabitId(long habitId) {
        this.habitId = habitId;
    }

    public String getReminderTime() {
        return reminderTime;
    }

    public void setReminderTime(String reminderTime) {
        this.reminderTime = reminderTime;
    }

    public String getDaysOfWeek() {
        return daysOfWeek;
    }

    public void setDaysOfWeek(String daysOfWeek) {
        this.daysOfWeek = daysOfWeek;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    /**
     * 检查指定日期是否需要提醒
     * @param dayOfWeek Calendar.DAY_OF_WEEK 值 (1=周日, 2=周一...7=周六)
     */
    public boolean shouldRemindOnDay(int dayOfWeek) {
        if (daysOfWeek == null || daysOfWeek.isEmpty()) return false;
        String[] days = daysOfWeek.split(",");
        for (String day : days) {
            if (Integer.parseInt(day.trim()) == dayOfWeek) {
                return true;
            }
        }
        return false;
    }
}
