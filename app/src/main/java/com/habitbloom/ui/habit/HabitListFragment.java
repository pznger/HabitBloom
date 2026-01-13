package com.habitbloom.ui.habit;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.habitbloom.R;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.ui.garden.PlantCardAdapter;
import com.habitbloom.ui.viewmodel.HabitViewModel;
import com.habitbloom.utils.Constants;

public class HabitListFragment extends Fragment implements HabitListAdapter.OnHabitClickListener {

    private RecyclerView recyclerHabits;
    private LinearLayout emptyState;
    private HabitViewModel habitViewModel;
    private HabitListAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_habit_list, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        initViews(view);
        initViewModel();
        setupRecyclerView();
        observeData();
    }

    private void initViews(View view) {
        recyclerHabits = view.findViewById(R.id.recycler_habits);
        emptyState = view.findViewById(R.id.empty_state);
    }

    private void initViewModel() {
        habitViewModel = new ViewModelProvider(this).get(HabitViewModel.class);
    }

    private void setupRecyclerView() {
        adapter = new HabitListAdapter(this);
        recyclerHabits.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerHabits.setAdapter(adapter);
    }

    private void observeData() {
        habitViewModel.getAllActiveHabits().observe(getViewLifecycleOwner(), habits -> {
            if (habits != null && !habits.isEmpty()) {
                adapter.setHabits(habits);
                recyclerHabits.setVisibility(View.VISIBLE);
                emptyState.setVisibility(View.GONE);
            } else {
                recyclerHabits.setVisibility(View.GONE);
                emptyState.setVisibility(View.VISIBLE);
            }
        });
    }

    @Override
    public void onHabitClick(Habit habit) {
        Intent intent = new Intent(getActivity(), HabitDetailActivity.class);
        intent.putExtra(Constants.EXTRA_HABIT_ID, habit.getHabitId());
        startActivity(intent);
    }
}
