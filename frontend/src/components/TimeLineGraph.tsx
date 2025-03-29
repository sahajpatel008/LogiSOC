import React from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartTooltip, ResponsiveContainer, Legend
} from 'recharts';
import { Paper, Typography, Box, Tooltip, IconButton } from '@mui/material';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

type Props = {
    title?: string;
    data: { time: string; count: number }[];
    infoText?: string; // ⬅️ Add info text prop
};

const TimeLineGraph: React.FC<Props> = ({ title = 'Timeline', data, infoText }) => {
    return (
        <Paper elevation={3} sx={{ p: 3, width: '100%', height: '100%' }}>
            {/* Title with optional info icon */}
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center', // ⬅️ This centers the title and icon
                    gap: 1,
                    mb: 2,
                }}
            >
                <Typography variant="h6">{title}</Typography>
                {infoText && (
                    <Tooltip title={infoText} arrow>
                        <IconButton size="small" sx={{ padding: 0 }}>
                            <InfoOutlinedIcon fontSize="small" />
                        </IconButton>
                    </Tooltip>
                )}
            </Box>


            <Box
                sx={{
                    width: '100%',
                    maxWidth: 500,
                    height: 300,
                    mx: 'auto',
                }}
            >
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" />
                        <YAxis />
                        <RechartTooltip />
                        <Legend />
                        <Line type="monotone" dataKey="count" stroke="#4caf50" strokeWidth={2} />
                    </LineChart>
                </ResponsiveContainer>
            </Box>
        </Paper>
    );
};

export default TimeLineGraph;
