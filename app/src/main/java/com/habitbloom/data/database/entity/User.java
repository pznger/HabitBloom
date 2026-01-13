package com.habitbloom.data.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "users")
public class User {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "user_id")
    private long userId;

    @ColumnInfo(name = "username")
    private String username = "用户";

    @ColumnInfo(name = "avatar_color")
    private String avatarColor = "#4CAF50";

    @ColumnInfo(name = "daily_goal_time")
    private String dailyGoalTime = "08:00";

    @ColumnInfo(name = "created_at")
    private long createdAt = System.currentTimeMillis();

    @ColumnInfo(name = "last_login")
    private Long lastLogin;

    // Getters and Setters
    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getAvatarColor() {
        return avatarColor;
    }

    public void setAvatarColor(String avatarColor) {
        this.avatarColor = avatarColor;
    }

    public String getDailyGoalTime() {
        return dailyGoalTime;
    }

    public void setDailyGoalTime(String dailyGoalTime) {
        this.dailyGoalTime = dailyGoalTime;
    }

    public long getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(long createdAt) {
        this.createdAt = createdAt;
    }

    public Long getLastLogin() {
        return lastLogin;
    }

    public void setLastLogin(Long lastLogin) {
        this.lastLogin = lastLogin;
    }
}
