package com.habitbloom.data.repository;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.dao.UserDao;
import com.habitbloom.data.database.entity.User;

public class UserRepository {
    private final UserDao userDao;

    public UserRepository(Application application) {
        AppDatabase db = AppDatabase.getDatabase(application);
        userDao = db.userDao();
    }

    public LiveData<User> getCurrentUser() {
        return userDao.getCurrentUser();
    }

    public User getCurrentUserSync() {
        return userDao.getCurrentUserSync();
    }

    public void updateUser(User user) {
        AppDatabase.databaseExecutor.execute(() -> userDao.update(user));
    }

    public void updateLastLogin() {
        AppDatabase.databaseExecutor.execute(() -> {
            User user = userDao.getCurrentUserSync();
            if (user != null) {
                userDao.updateLastLogin(user.getUserId(), System.currentTimeMillis());
            }
        });
    }

    public void createUserIfNotExists(Callback callback) {
        AppDatabase.databaseExecutor.execute(() -> {
            int count = userDao.getUserCount();
            if (count == 0) {
                User user = new User();
                user.setUsername("用户");
                user.setAvatarColor("#4CAF50");
                user.setCreatedAt(System.currentTimeMillis());
                userDao.insert(user);
            }
            if (callback != null) {
                callback.onComplete();
            }
        });
    }

    public interface Callback {
        void onComplete();
    }
}
