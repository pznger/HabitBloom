package com.habitbloom.data.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "garden_states",
        foreignKeys = {
                @ForeignKey(
                        entity = User.class,
                        parentColumns = "user_id",
                        childColumns = "user_id",
                        onDelete = ForeignKey.CASCADE
                ),
                @ForeignKey(
                        entity = Habit.class,
                        parentColumns = "habit_id",
                        childColumns = "habit_id",
                        onDelete = ForeignKey.CASCADE
                )
        },
        indices = {@Index("user_id"), @Index("habit_id")})
public class GardenState {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "state_id")
    private long stateId;

    @ColumnInfo(name = "user_id")
    private long userId = 1;

    @ColumnInfo(name = "habit_id")
    private long habitId;

    @ColumnInfo(name = "plant_growth")
    private int plantGrowth = 0; // 0-100

    @ColumnInfo(name = "plant_health")
    private int plantHealth = 100; // 0-100

    @ColumnInfo(name = "last_watered")
    private String lastWatered; // yyyy-MM-dd

    @ColumnInfo(name = "stage")
    private int stage = 1; // 1=种子, 2=发芽, 3=幼苗, 4=开花, 5=结果

    // Getters and Setters
    public long getStateId() {
        return stateId;
    }

    public void setStateId(long stateId) {
        this.stateId = stateId;
    }

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }

    public long getHabitId() {
        return habitId;
    }

    public void setHabitId(long habitId) {
        this.habitId = habitId;
    }

    public int getPlantGrowth() {
        return plantGrowth;
    }

    public void setPlantGrowth(int plantGrowth) {
        this.plantGrowth = Math.max(0, Math.min(100, plantGrowth));
    }

    public int getPlantHealth() {
        return plantHealth;
    }

    public void setPlantHealth(int plantHealth) {
        this.plantHealth = Math.max(0, Math.min(100, plantHealth));
    }

    public String getLastWatered() {
        return lastWatered;
    }

    public void setLastWatered(String lastWatered) {
        this.lastWatered = lastWatered;
    }

    public int getStage() {
        return stage;
    }

    public void setStage(int stage) {
        this.stage = Math.max(1, Math.min(5, stage));
    }

    public String getStageName() {
        switch (stage) {
            case 1: return "种子";
            case 2: return "发芽";
            case 3: return "幼苗";
            case 4: return "开花";
            case 5: return "结果";
            default: return "种子";
        }
    }

    public String getHealthStatus() {
        if (plantHealth >= 80) return "茂盛";
        if (plantHealth >= 50) return "健康";
        if (plantHealth >= 20) return "需要照顾";
        return "缺水";
    }
}
