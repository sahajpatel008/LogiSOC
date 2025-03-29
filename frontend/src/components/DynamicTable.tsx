// src/components/DynamicTable.tsx
import React from 'react';
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography, Box,
  Tooltip, IconButton
} from '@mui/material';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

type Props = {
  title?: string;
  columns: string[];
  rows: any[][];
  infoText?: string; // optional tooltip text
};

const DynamicTable: React.FC<Props> = ({ title = 'Table', columns, rows, infoText }) => {
  return (
    <TableContainer
      component={Paper}
      sx={{
        mb: 4,
        maxHeight: 500,
        overflowY: 'auto',
        border: 'none',
        borderRight: '1px solid #e0e0e0',
        boxShadow: 'none',
      }}
    >
      {title && (
        <Box
          sx={{
            position: 'sticky',
            top: 0,
            zIndex: 2,
            backgroundColor: 'white',
            borderBottom: '1px solid #ccc',
            p: 2,
            display: 'flex',
            alignItems: 'center',
            gap: 1,
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
      )}
      <Table
        stickyHeader
        sx={{
          border: 'none',
          '& td, & th': {
            border: 'none',
          },
        }}
      >
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
