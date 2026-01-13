package com.habitbloom.ui.settings;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.google.android.material.card.MaterialCardView;
import com.google.android.material.switchmaterial.SwitchMaterial;
import com.habitbloom.R;
import com.habitbloom.ui.viewmodel.UserViewModel;
import com.habitbloom.utils.Constants;

public class SettingsFragment extends Fragment {

    private MaterialCardView cardProfile;
    private TextView tvUsername;
    private SwitchMaterial switchDarkMode;
    private View itemNotification;
    private View itemExport;
    private View itemImport;
    private View itemClear;
    private View itemAbout;
    private TextView tvVersion;

    private UserViewModel userViewModel;
    private SharedPreferences preferences;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_settings, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        initViews(view);
        initViewModel();
        initPreferences();
        setupListeners();
        observeData();
    }

    private void initViews(View view) {
        cardProfile = view.findViewById(R.id.card_profile);
        tvUsername = view.findViewById(R.id.tv_username);
        switchDarkMode = view.findViewById(R.id.switch_dark_mode);
        itemNotification = view.findViewById(R.id.item_notification);
        itemExport = view.findViewById(R.id.item_export);
        itemImport = view.findViewById(R.id.item_import);
        itemClear = view.findViewById(R.id.item_clear);
        itemAbout = view.findViewById(R.id.item_about);
        tvVersion = view.findViewById(R.id.tv_version);

        tvVersion.setText(getString(R.string.version, "1.0.0"));
    }

    private void initViewModel() {
        userViewModel = new ViewModelProvider(this).get(UserViewModel.class);
    }

    private void initPreferences() {
        preferences = requireContext().getSharedPreferences(Constants.PREF_NAME, 0);
        boolean isDarkMode = preferences.getBoolean(Constants.PREF_DARK_MODE, false);
        switchDarkMode.setChecked(isDarkMode);
    }

    private void setupListeners() {
        cardProfile.setOnClickListener(v -> {
            // TODO: Open profile edit dialog
            Toast.makeText(getContext(), "个人资料编辑功能开发中", Toast.LENGTH_SHORT).show();
        });

        switchDarkMode.setOnCheckedChangeListener((buttonView, isChecked) -> {
            preferences.edit().putBoolean(Constants.PREF_DARK_MODE, isChecked).apply();
            AppCompatDelegate.setDefaultNightMode(
                    isChecked ? AppCompatDelegate.MODE_NIGHT_YES : AppCompatDelegate.MODE_NIGHT_NO
            );
        });

        itemNotification.setOnClickListener(v -> {
            Toast.makeText(getContext(), "通知设置功能开发中", Toast.LENGTH_SHORT).show();
        });

        itemExport.setOnClickListener(v -> {
            Toast.makeText(getContext(), "数据导出功能开发中", Toast.LENGTH_SHORT).show();
        });

        itemImport.setOnClickListener(v -> {
            Toast.makeText(getContext(), "数据导入功能开发中", Toast.LENGTH_SHORT).show();
        });

        itemClear.setOnClickListener(v -> showClearDataDialog());

        itemAbout.setOnClickListener(v -> showAboutDialog());
    }

    private void observeData() {
        userViewModel.getCurrentUser().observe(getViewLifecycleOwner(), user -> {
            if (user != null) {
                tvUsername.setText(user.getUsername());
            }
        });
    }

    private void showClearDataDialog() {
        new AlertDialog.Builder(requireContext())
                .setTitle(R.string.confirm_delete)
                .setMessage(R.string.confirm_clear_data)
                .setPositiveButton(R.string.confirm, (dialog, which) -> {
                    // TODO: Clear all data
                    Toast.makeText(getContext(), "数据清除功能开发中", Toast.LENGTH_SHORT).show();
                })
                .setNegativeButton(R.string.cancel, null)
                .show();
    }

    private void showAboutDialog() {
        new AlertDialog.Builder(requireContext())
                .setTitle(R.string.app_name)
                .setMessage("HabitBloom 是一款基于可视化花园的个人习惯养成应用。\n\n" +
                        "通过每日完成习惯来\"浇灌\"你的习惯花园，让好习惯如花般绽放！\n\n" +
                        "版本: 1.0.0\n" +
                        "© 2026 HabitBloom Team")
                .setPositiveButton("确定", null)
                .show();
    }
}
