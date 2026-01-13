package com.habitbloom.ui.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.habitbloom.data.database.entity.User;
import com.habitbloom.data.repository.UserRepository;

public class UserViewModel extends AndroidViewModel {
    private final UserRepository userRepository;
    private final LiveData<User> currentUser;

    public UserViewModel(@NonNull Application application) {
        super(application);
        userRepository = new UserRepository(application);
        currentUser = userRepository.getCurrentUser();
    }

    public LiveData<User> getCurrentUser() {
        return currentUser;
    }

    public void updateUser(User user) {
        userRepository.updateUser(user);
    }

    public void updateLastLogin() {
        userRepository.updateLastLogin();
    }

    public void ensureUserExists(UserRepository.Callback callback) {
        userRepository.createUserIfNotExists(callback);
    }
}
