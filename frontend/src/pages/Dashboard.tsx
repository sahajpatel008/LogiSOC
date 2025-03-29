import React, { useState } from 'react';
import axios from 'axios';
import DynamicTable from '../components/DynamicTable';
import FileUpload from '../components/FileUpload'; // 👈 your upload component
import { useAuth } from '@clerk/clerk-react';
import { CircularProgress, Typography } from '@mui/material';

const Dashboard = () => {
  const { getToken } = useAuth();
  const [dataSets, setDataSets] = useState<{ columns: string[]; rows: any[][] }[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasUploaded, setHasUploaded] = useState(false);

  const fetchAllTablesInOrder = async () => {
    setLoading(true);
    const token = await getToken();

    const urls = [
      'http://127.0.0.1:5000/top-referers',
      'http://127.0.0.1:5000/top-page-visits',
      // Add other URLs here
    ];

    const results: { columns: string[]; rows: any[][] }[] = [];

    for (const url of urls) {
      try {
        const res = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        results.push(res.data);
      } catch (err) {
        console.error(`Error fetching ${url}:`, err);
        results.push({ columns: [], rows: [] });
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
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      setHasUploaded(true);
      fetchAllTablesInOrder();
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  const tableTitles = [
    'Top Referers',
    'Top Page Visits',
    'Malicious Domains',
    'Request Status',
    // ...
  ];

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
        dataSets.map((data, idx) => (
          <DynamicTable
            key={idx}
            title={tableTitles[idx]}
            columns={data.columns}
            rows={data.rows}
          />
        ))
      )}
    </div>
  );
};

export default Dashboard;
