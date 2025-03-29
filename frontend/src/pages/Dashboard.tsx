import React, { useState } from 'react';
import axios from 'axios';
import DynamicTable from '../components/DynamicTable';
import FileUpload from '../components/FileUpload';
import { useAuth } from '@clerk/clerk-react';
import {
  CircularProgress,
  Typography,
  Paper,
  Collapse,
  Button,
  Container,
  Box,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import PieChartComponent from '../components/PieChart';
import TimeLineGraph from '../components/TimeLineGraph';

type DataSet = {
  title: string;
  columns?: string[];
  rows?: any[][];
  data?: { time: string; count: number }[];
  infoText?: string; // ⬅️ add this
};


const Dashboard = () => {
  const { getToken } = useAuth();
  const [dataSets, setDataSets] = useState<DataSet[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasUploaded, setHasUploaded] = useState(false);
  const [showUploadBox, setShowUploadBox] = useState(true);

  const fetchAllTablesInOrder = async () => {
    setLoading(true);
    const token = await getToken();

    const urls = [
      'http://127.0.0.1:5000/top-referers',
      'http://127.0.0.1:5000/top-page-visits',
      'http://127.0.0.1:5000/check-domains',
      'http://127.0.0.1:5000/request-status',
      'http://127.0.0.1:5000/404-error-ips',
      'http://127.0.0.1:5000/429-error-ips',
      'http://127.0.0.1:5000/burstActivity',
      'http://127.0.0.1:5000/get-data-exfiltration',
      'http://127.0.0.1:5000/activity-timeline',
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
        } else if (data && Array.isArray(data.data)) {
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
      setShowUploadBox(false);
      fetchAllTablesInOrder();
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Paper elevation={0} sx={{ mb: 4, p: 3 }}>
        <Collapse in={showUploadBox}>
          <FileUpload onUpload={handleFileUpload} />
        </Collapse>
        {hasUploaded && !showUploadBox && (
          <Box sx={{ mt: 2 }}>
            <Button variant="outlined" onClick={() => setShowUploadBox(true)}>
              Upload another file
            </Button>
          </Box>
        )}
      </Paper>

      {!hasUploaded ? (
        <Typography variant="body1" sx={{ mt: 2 }}>
          Please upload a file to begin analysis.
        </Typography>
      ) : loading ? (
        <CircularProgress sx={{ mt: 4 }} />
      ) : (
        <>
          {/* Top charts row */}
          {/* Top charts row */}
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              flexWrap: 'wrap',
              gap: 3,
              mb: 5, // ⬅️ increase this
              pb: 2, // ⬅️ optional padding below
            }}
          >
            {dataSets[3]?.rows && (
              <Box sx={{
                p: 2,
                backgroundImage: 'none', // removes gradient background
                boxShadow: 'none',        // removes shadow if elevation isn't enough
                border: 'none',           // removes any accidental border
              }}>
                <PieChartComponent
                  title={dataSets[3].title}
                  data={dataSets[3].rows.map((row: any[]) => ({
                    name: row[0],
                    value: row[1],
                  }))}
                />
              </Box>
            )}

            {dataSets[8]?.data && (
              <Box sx={{
                p: 2,
                backgroundImage: 'none', // removes gradient background
                boxShadow: 'none',        // removes shadow if elevation isn't enough
                border: 'none',           // removes any accidental border
              }}>
                <TimeLineGraph
                  title={dataSets[8].title}
                  data={dataSets[8].data}
                />
              </Box>
            )}
          </Box>

          {/* Top Tables Row (3 columns) */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            {[0, 1, 4].map((idx) => {
              const data = dataSets[idx];
              return (
                <Grid
                  item
                  xs={12}
                  sm={6}
                  md={4}
                  key={idx}
                  component="div"
                  {...({} as any)}
                >
                  <Box
                    sx={{
                      p: 2,
                      height: '100%',
                      borderRadius: 2,
                      boxShadow: 1,
                      backgroundColor: 'background.paper',
                    }}
                  >
                    <DynamicTable
                      title={data.title}
                      columns={data.columns || []}
                      rows={data.rows || []}
                      infoText={data.infoText}
                    />
                  </Box>
                </Grid>
              );
            })}
          </Grid>

          {/* Grouped Box for Check Domains + Burst Activity */}
          <Box
            sx={{
              border: '1px solid #ddd',
              borderRadius: 2,
              p: 2,
              mb: 4,
              backgroundColor: 'background.paper',
            }}
          >
            <Grid container spacing={3}>
              {[2, 6].map((idx) => {
                const data = dataSets[idx];
                return (
                  <Grid
                    item
                    xs={12}
                    sm={6}
                    key={idx}
                    component="div"
                    {...({} as any)}
                  >
                    <Box
                      sx={{
                        p: 2,
                        height: '100%',
                        borderRadius: 1,
                        boxShadow: 1,
                        backgroundColor: 'background.paper',
                      }}
                    >
                      <DynamicTable
                        title={data.title}
                        columns={data.columns || []}
                        rows={data.rows || []}
                        infoText={data.infoText}
                      />
                    </Box>
                  </Grid>
                );
              })}
            </Grid>
          </Box>



          {/* Rest of the data as tables */}
          <Grid container spacing={4}>
            {dataSets.map((data, idx) => {
              // Skip charts and the 3 top tables already shown
              if ([0, 1, 2, 3, 4, 6, 8].includes(idx)) return null;

              let content = null;

              if (data.columns && data.rows) {
                content = (
                  <DynamicTable
                    title={data.title}
                    columns={data.columns}
                    rows={data.rows}
                    infoText={data.infoText}
                  />
                );
              } else {
                content = (
                  <Typography variant="body2" color="error">
                    Could not load table data for: {data.title || `Dataset ${idx + 1}`}
                  </Typography>
                );
              }

              return (
                <Grid
                  item
                  xs={12}
                  sm={6}
                  md={4}
                  key={idx}
                  component="div"
                  {...({} as any)}
                >
                  <Box
                    sx={{
                      p: 2,
                      height: '100%',
                      borderRadius: 2,
                      boxShadow: 1,
                      backgroundColor: 'background.paper',
                    }}
                  >
                    {content}
                  </Box>
                </Grid>
              );
            })}
          </Grid>

        </>
      )}
    </Container>
  );
};

export default Dashboard;
