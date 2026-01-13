package com.habitbloom.data.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "habit_records",
        foreignKeys = @ForeignKey(
                entity = Habit.class,
                parentColumns = "habit_id",
                childColumns = "habit_id",
                onDelete = ForeignKey.CASCADE
        ),
        indices = {@Index("habit_id"), @Index("record_date"), @Index(value = {"habit_id", "record_date"}, unique = true)})
public class HabitRecord {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "record_id")
    private long recordId;

    @ColumnInfo(name = "habit_id")
    private long habitId;

    @ColumnInfo(name = "record_date")
    private String recordDate; // yyyy-MM-dd

    @ColumnInfo(name = "completed")
    private boolean completed = false;

    @ColumnInfo(name = "completed_time")
    private String completedTime; // HH:mm

    @ColumnInfo(name = "notes")
    private String notes;

    @ColumnInfo(name = "plant_growth_stage")
    private int plantGrowthStage = 0;

    // Getters and Setters
    public long getRecordId() {
        return recordId;
    }

    public void setRecordId(long recordId) {
        this.recordId = recordId;
    }

    public long getHabitId() {
        return habitId;
    }

    public void setHabitId(long habitId) {
        this.habitId = habitId;
    }

    public String getRecordDate() {
        return recordDate;
    }

    public void setRecordDate(String recordDate) {
        this.recordDate = recordDate;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public String getCompletedTime() {
        return completedTime;
    }

    public void setCompletedTime(String completedTime) {
        this.completedTime = completedTime;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }

    public int getPlantGrowthStage() {
        return plantGrowthStage;
    }

    public void setPlantGrowthStage(int plantGrowthStage) {
        this.plantGrowthStage = plantGrowthStage;
    }
}
