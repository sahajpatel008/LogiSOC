import React, { useState } from 'react';
import axios from 'axios';
import DynamicTable from '../components/DynamicTable';
import FileUpload from '../components/FileUpload';
import { useAuth } from '@clerk/clerk-react';
import { CircularProgress, Typography } from '@mui/material';
import PieChartComponent from '../components/PieChart';

type DataSet = {
  title: string;
  columns?: string[];
  rows?: any[][];
};

const Dashboard = () => {
  const { getToken } = useAuth();
  const [dataSets, setDataSets] = useState<DataSet[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasUploaded, setHasUploaded] = useState(false);

  const fetchAllTablesInOrder = async () => {
    setLoading(true);
    const token = await getToken();

    const urls = [
        'http://127.0.0.1:5000/top-referers',
        'http://127.0.0.1:5000/top-page-visits',
        'http://127.0.0.1:5000/check-domains',
        'http://127.0.0.1:5000/request-status', // ⬅️ Pie Chart
        'http://127.0.0.1:5000/404-error-ips',
        'http://127.0.0.1:5000/429-error-ips',
        'http://127.0.0.1:5000/burstActivity',
        'http://127.0.0.1:5000/get-data-exfiltration',
    ];

    const results: DataSet[] = [];

    for (const url of urls) {
      try {
        const res = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = res.data;

        if (data && Array.isArray(data.columns) && Array.isArray(data.rows)) {
          results.push(data);
        } else {
          console.warn(`Malformed response from ${url}:`, data);
          results.push({ title: 'Malformed Data', columns: [], rows: [] });
        }
      } catch (err) {
        console.error(`Error fetching ${url}:`, err);
        results.push({ title: 'Error', columns: [], rows: [] });
      }
    }

    setDataSets(results);
    setLoading(false);
  };

  const handleFileUpload = async (file: File) => {
    const token = await getToken();
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      setHasUploaded(true);
      fetchAllTablesInOrder();
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  return (
    <div className="space-y-10">
      <FileUpload onUpload={handleFileUpload} />

      {!hasUploaded ? (
        <Typography variant="body1" sx={{ mt: 2 }}>
          Please upload a file to begin analysis.
        </Typography>
      ) : loading ? (
        <CircularProgress sx={{ mt: 4 }} />
      ) : (
        dataSets.map((data, idx) => {
          if (idx === 3 && data.rows) {
            const pieData = data.rows.map((row: any[]) => ({
              name: row[0],
              value: row[1],
            }));

            return (
              <PieChartComponent
                key={idx}
                title={data.title}
                data={pieData}
              />
            );
          }

          if (data.columns && data.rows) {
            return (
              <DynamicTable
                key={idx}
                title={data.title}
                columns={data.columns}
                rows={data.rows}
              />
            );
          } else {
            return (
              <Typography key={idx} variant="body2" color="error">
                Could not load table data for: {data.title || `Dataset ${idx + 1}`}
              </Typography>
            );
          }
        })
      )}
    </div>
  );
};

export default Dashboard;
