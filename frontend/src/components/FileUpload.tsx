// src/components/FileUpload.tsx
import React, { useRef, useState } from 'react';
import {
  Box, Button, Typography, Paper, Stack
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';

type Props = {
  onUpload: (file: File) => void;
  acceptedTypes?: string;
};

const FileUpload: React.FC<Props> = ({ onUpload, acceptedTypes = '.csv,.log,.txt' }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      const file = e.target.files[0];
      setSelectedFile(file);
    }
  };

  const handleUploadClick = () => {
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, textAlign: 'center' }}>
      <Typography variant="h6" gutterBottom>
        Upload a Log File
      </Typography>

      <input
        type="file"
        accept={acceptedTypes}
        hidden
        ref={fileInputRef}
        onChange={handleFileSelect}
      />

      <Stack spacing={2} alignItems="center">
        <Button
          variant="outlined"
          startIcon={<UploadFileIcon />}
          onClick={() => fileInputRef.current?.click()}
        >
          Choose File
        </Button>

        {selectedFile && (
          <Typography variant="body2" color="textSecondary">
            Selected: {selectedFile.name}
          </Typography>
        )}

        <Button
          variant="contained"
          color="primary"
          onClick={handleUploadClick}
          disabled={!selectedFile}
        >
          Upload
        </Button>
      </Stack>
    </Paper>
  );
};

export default FileUpload;
