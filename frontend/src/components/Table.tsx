import React from 'react';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Typography
} from '@mui/material';

type Column = {
  id: string;
  label: string;
  render?: (value: any, row?: Record<string, any>) => React.ReactNode;
};

type Props = {
  title?: string;
  columns?: Column[];
  rows?: Record<string, any>[]; // Now optional
};

// 🧩 Default Column Definitions
const defaultColumns: Column[] = [
  { id: 'domain', label: 'Domain' },
  { id: 'isMalicious', label: 'Malicious' },
  { id: 'category', label: 'Category' },
  { id: 'threatType', label: 'Threat Type' },
];

// 📦 Default Sample Rows
const defaultRows: Record<string, any>[] = [
  {
    domain: 'malicious-site.com',
    isMalicious: 'TRUE',
    category: 'Phishing',
    threatType: 'Credential Theft',
  },
  {
    domain: 'suspicious-link.net',
    isMalicious: 'TRUE',
    category: 'Malware',
    threatType: 'Trojan',
  },
  {
    domain: 'safe-website.org',
    isMalicious: 'FALSE',
    category: 'Safe',
    threatType: '-',
  },
];

const CustomTable: React.FC<Props> = ({
  title = 'Malicious Domains Table',
  columns = defaultColumns,
  rows = defaultRows
}) => {
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
            {columns.map((col) => (
              <TableCell key={col.id}>{col.label}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              {columns.map((col) => (
                <TableCell key={col.id}>
                  {col.render ? col.render(row[col.id], row) : row[col.id]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CustomTable;
