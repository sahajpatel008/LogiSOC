// src/components/DynamicTable.tsx
import React from 'react';
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography, Box
} from '@mui/material';

type Props = {
  title?: string;
  columns: string[];
  rows: any[][];
};

const DynamicTable: React.FC<Props> = ({ title = 'Table', columns, rows }) => {
  return (
    <TableContainer component={Paper} sx={{
      mb: 4,
      maxHeight: 500,
      overflowY: 'auto'
    }}>
      {title && (
  <Box
    sx={{
      position: 'sticky',
      top: 0,
      zIndex: 2,
      backgroundColor: 'white', // match your Paper bg
      borderBottom: '1px solid #ccc',
      p: 2,
    }}
  >
    <Typography variant="h6">{title}</Typography>
  </Box>
)}
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {columns.map((col, idx) => (
              <TableCell key={idx}>{col}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, rowIdx) => (
            <TableRow key={rowIdx}>
              {row.map((cell, colIdx) => (
                <TableCell key={colIdx}>{cell}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default DynamicTable;
