import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { Paper, Typography, Box } from '@mui/material';

type Props = {
  title?: string;
  data: { time: string; count: number }[];
};

const TimeLineGraph: React.FC<Props> = ({ title = 'Timeline', data }) => {
  return (
    <Paper elevation={3} sx={{ p: 3, width: '100%', height: '100%' }}>
  <Typography variant="h6" gutterBottom>{title}</Typography>
  <Box
    sx={{
      width: '100%',
      maxWidth: 500,     // ⬅️ NEW: Set a max width
      height: 300,
      mx: 'auto',        // ⬅️ NEW: Center horizontally if narrower
    }}
  >
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="count" stroke="#4caf50" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  </Box>
</Paper>
  );
};

export default TimeLineGraph;
