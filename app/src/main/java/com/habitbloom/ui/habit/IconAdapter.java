package com.habitbloom.ui.habit;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.habitbloom.R;

public class IconAdapter extends RecyclerView.Adapter<IconAdapter.IconViewHolder> {

    private final String[] icons;
    private final OnIconClickListener listener;
    private int selectedPosition = 0;

    public interface OnIconClickListener {
        void onIconClick(String icon);
    }

    public IconAdapter(String[] icons, OnIconClickListener listener) {
        this.icons = icons;
        this.listener = listener;
    }

    @NonNull
    @Override
    public IconViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_icon, parent, false);
        return new IconViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull IconViewHolder holder, int position) {
        holder.bind(icons[position], position == selectedPosition);
    }

    @Override
    public int getItemCount() {
        return icons.length;
    }

    class IconViewHolder extends RecyclerView.ViewHolder {
        private final FrameLayout container;
        private final TextView tvIcon;

        IconViewHolder(@NonNull View itemView) {
            super(itemView);
            container = itemView.findViewById(R.id.icon_container);
            tvIcon = itemView.findViewById(R.id.tv_icon);
        }

        void bind(String icon, boolean isSelected) {
            tvIcon.setText(icon);
            
            if (isSelected) {
                tvIcon.setBackgroundResource(R.drawable.icon_selected_background);
            } else {
                tvIcon.setBackgroundResource(R.drawable.circle_background);
            }

            itemView.setOnClickListener(v -> {
                int previousPosition = selectedPosition;
                selectedPosition = getAdapterPosition();
                notifyItemChanged(previousPosition);
                notifyItemChanged(selectedPosition);
                
                if (listener != null) {
                    listener.onIconClick(icon);
                }
            });
        }
    }
}
