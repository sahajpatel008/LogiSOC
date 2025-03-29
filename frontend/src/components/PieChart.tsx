import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Paper, Typography } from '@mui/material';

type Props = {
  title?: string;
  data: { name: string; value: number }[];
};

// 🎨 Exact status-to-color mapping
const STATUS_COLORS: Record<string, string> = {
  allowed: '#4caf50',       // Green
  blocked: '#f44336',       // Red
  'server error': '#ff9800', // Orange
  other: '#90a4ae',         // Gray/Blue
};

const fallbackColor = '#bdbdbd';

const PieChartComponent: React.FC<Props> = ({ title = "Traffic Classification", data }) => {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={100}
            dataKey="value"
            label
          >
            {data.map((entry, index) => {
              const name = entry.name.toLowerCase();
              const color = STATUS_COLORS[name] || fallbackColor;
              return <Cell key={`cell-${index}`} fill={color} />;
            })}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  );
};

export default PieChartComponent;
