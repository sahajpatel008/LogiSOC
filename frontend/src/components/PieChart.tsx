// src/components/PieChartComponent.jsx
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Paper, Typography } from '@mui/material';

const data = [
  { name: 'Blocked', value: 400 },
  { name: 'Allowed', value: 300 },
  { name: 'Suspicious', value: 300 },
  { name: 'Unknown', value: 200 },
];

const COLORS = ['#e57373', '#81c784', '#ffd54f', '#64b5f6'];

const PieChartComponent = () => {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Traffic Classification
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
            label
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  );
};

export default PieChartComponent;
