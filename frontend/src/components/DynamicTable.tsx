// src/components/DynamicTable.tsx
import React from 'react';
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography
} from '@mui/material';

type Props = {
  title?: string;
  columns: string[];
  rows: any[][];
};

const DynamicTable: React.FC<Props> = ({ title = 'Table', columns, rows }) => {
  return (
    <TableContainer component={Paper} sx={{ mb: 4 }}>
      {title && (
        <Typography variant="h6" sx={{ p: 2 }}>
          {title}
        </Typography>
      )}
      <Table>
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
