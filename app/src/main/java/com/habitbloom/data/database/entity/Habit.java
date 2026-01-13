package com.habitbloom.data.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "habits",
        foreignKeys = @ForeignKey(
                entity = User.class,
                parentColumns = "user_id",
                childColumns = "user_id",
                onDelete = ForeignKey.CASCADE
        ),
        indices = {@Index("user_id"), @Index("category")})
public class Habit {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "habit_id")
    private long habitId;

    @ColumnInfo(name = "user_id")
    private long userId = 1;

    @ColumnInfo(name = "name")
    private String name;

    @ColumnInfo(name = "category")
    private String category = "life"; // health, study, work, life

    @ColumnInfo(name = "icon")
    private String icon = "🌱";

    @ColumnInfo(name = "plant_type")
    private String plantType = "flower"; // flower, tree, cactus, herb

    @ColumnInfo(name = "target_frequency")
    private int targetFrequency = 7; // 每周目标次数

    @ColumnInfo(name = "current_streak")
    private int currentStreak = 0;

    @ColumnInfo(name = "longest_streak")
    private int longestStreak = 0;

    @ColumnInfo(name = "total_completed")
    private int totalCompleted = 0;

    @ColumnInfo(name = "difficulty")
    private int difficulty = 3; // 1-5

    @ColumnInfo(name = "is_active")
    private boolean isActive = true;

    @ColumnInfo(name = "created_at")
    private long createdAt = System.currentTimeMillis();

    // Getters and Setters
    public long getHabitId() {
        return habitId;
    }

    public void setHabitId(long habitId) {
        this.habitId = habitId;
    }

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getIcon() {
        return icon;
    }

    public void setIcon(String icon) {
        this.icon = icon;
    }

    public String getPlantType() {
        return plantType;
    }

    public void setPlantType(String plantType) {
        this.plantType = plantType;
    }

    public int getTargetFrequency() {
        return targetFrequency;
    }

    public void setTargetFrequency(int targetFrequency) {
        this.targetFrequency = targetFrequency;
    }

    public int getCurrentStreak() {
        return currentStreak;
    }

    public void setCurrentStreak(int currentStreak) {
        this.currentStreak = currentStreak;
    }

    public int getLongestStreak() {
        return longestStreak;
    }

    public void setLongestStreak(int longestStreak) {
        this.longestStreak = longestStreak;
    }

    public int getTotalCompleted() {
        return totalCompleted;
    }

    public void setTotalCompleted(int totalCompleted) {
        this.totalCompleted = totalCompleted;
    }

    public int getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(int difficulty) {
        this.difficulty = difficulty;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public long getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(long createdAt) {
        this.createdAt = createdAt;
    }

    // Helper methods
    public String getCategoryDisplayName() {
        switch (category) {
            case "health": return "健康";
            case "study": return "学习";
            case "work": return "工作";
            case "life": return "生活";
            default: return "其他";
        }
    }

    public String getPlantTypeDisplayName() {
        switch (plantType) {
            case "flower": return "花朵";
            case "tree": return "树木";
            case "cactus": return "仙人掌";
            case "herb": return "草本";
            default: return "植物";
        }
    }

    /**
     * 根据连续天数计算生长阶段
     * 1=种子, 2=发芽, 3=幼苗, 4=开花, 5=结果
     */
    public int getGrowthStage() {
        if (currentStreak >= 66) return 5;
        if (currentStreak >= 21) return 4;
        if (currentStreak >= 7) return 3;
        if (currentStreak >= 3) return 2;
        return 1;
    }

    public String getGrowthStageName() {
        switch (getGrowthStage()) {
            case 1: return "种子";
            case 2: return "发芽";
            case 3: return "幼苗";
            case 4: return "开花";
            case 5: return "结果";
            default: return "种子";
        }
    }
}
