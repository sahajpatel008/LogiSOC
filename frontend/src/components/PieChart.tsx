import { PieChart, Pie, Cell, Tooltip as RechartTooltip, Legend, ResponsiveContainer } from 'recharts';
import { Paper, Typography, Box, IconButton, Tooltip } from '@mui/material';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

type Props = {
  title?: string;
  data: { name: string; value: number }[];
  infoText?: string; // ⬅️ Optional tooltip prop
};

// 🎨 Exact status-to-color mapping
const STATUS_COLORS: Record<string, string> = {
  allowed: '#4caf50',
  blocked: '#f44336',
  'server error': '#ff9800',
  other: '#90a4ae',
};

const fallbackColor = '#bdbdbd';

const PieChartComponent: React.FC<Props> = ({ title = "Traffic Classification", data, infoText }) => {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
        <Typography variant="h6">{title}</Typography>
        {infoText && (
          <Tooltip title={infoText} arrow>
            <IconButton size="small" sx={{ padding: 0 }}>
              <InfoOutlinedIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        )}
      </Box>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={70}
            dataKey="value"
            label
          >
            {data.map((entry, index) => {
              const name = entry.name.toLowerCase();
              const color = STATUS_COLORS[name] || fallbackColor;
              return <Cell key={`cell-${index}`} fill={color} />;
            })}
          </Pie>
          <RechartTooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  );
};

export default PieChartComponent;
