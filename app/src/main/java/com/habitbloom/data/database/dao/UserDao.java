package com.habitbloom.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;

import com.habitbloom.data.database.entity.User;

import java.util.List;

@Dao
public interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    long insert(User user);

    @Update
    void update(User user);

    @Delete
    void delete(User user);

    @Query("SELECT * FROM users WHERE user_id = :userId")
    LiveData<User> getUserById(long userId);

    @Query("SELECT * FROM users WHERE user_id = :userId")
    User getUserByIdSync(long userId);

    @Query("SELECT * FROM users LIMIT 1")
    LiveData<User> getCurrentUser();

    @Query("SELECT * FROM users LIMIT 1")
    User getCurrentUserSync();

    @Query("SELECT * FROM users")
    List<User> getAllUsersSync();

    @Query("UPDATE users SET last_login = :timestamp WHERE user_id = :userId")
    void updateLastLogin(long userId, long timestamp);

    @Query("SELECT COUNT(*) FROM users")
    int getUserCount();
}
