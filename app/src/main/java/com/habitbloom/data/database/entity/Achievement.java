package com.habitbloom.data.database.entity;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

@Entity(tableName = "achievements",
        foreignKeys = @ForeignKey(
                entity = User.class,
                parentColumns = "user_id",
                childColumns = "user_id",
                onDelete = ForeignKey.CASCADE
        ),
        indices = {@Index("user_id")})
public class Achievement {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "achievement_id")
    private long achievementId;

    @ColumnInfo(name = "user_id")
    private long userId = 1;

    @ColumnInfo(name = "achievement_type")
    private String achievementType;

    @ColumnInfo(name = "title")
    private String title;

    @ColumnInfo(name = "description")
    private String description;

    @ColumnInfo(name = "badge_icon")
    private String badgeIcon;

    @ColumnInfo(name = "unlocked_at")
    private Long unlockedAt; // null表示未解锁

    @ColumnInfo(name = "requirement_value")
    private int requirementValue;

    // Getters and Setters
    public long getAchievementId() {
        return achievementId;
    }

    public void setAchievementId(long achievementId) {
        this.achievementId = achievementId;
    }

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }

    public String getAchievementType() {
        return achievementType;
    }

    public void setAchievementType(String achievementType) {
        this.achievementType = achievementType;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getBadgeIcon() {
        return badgeIcon;
    }

    public void setBadgeIcon(String badgeIcon) {
        this.badgeIcon = badgeIcon;
    }

    public Long getUnlockedAt() {
        return unlockedAt;
    }

    public void setUnlockedAt(Long unlockedAt) {
        this.unlockedAt = unlockedAt;
    }

    public int getRequirementValue() {
        return requirementValue;
    }

    public void setRequirementValue(int requirementValue) {
        this.requirementValue = requirementValue;
    }

    public boolean isUnlocked() {
        return unlockedAt != null;
    }

    // 预定义成就类型
    public static final String TYPE_STREAK_7 = "streak_7";
    public static final String TYPE_STREAK_21 = "streak_21";
    public static final String TYPE_STREAK_66 = "streak_66";
    public static final String TYPE_TOTAL_10 = "total_10";
    public static final String TYPE_TOTAL_50 = "total_50";
    public static final String TYPE_TOTAL_100 = "total_100";
    public static final String TYPE_PERFECT_WEEK = "perfect_week";
    public static final String TYPE_FIRST_HABIT = "first_habit";
    public static final String TYPE_HABIT_MASTER = "habit_master";
}
