import React from 'react';
import { Card, CardActionArea, CardMedia, CardContent, Typography, Box, Paper } from '@mui/material';
import { Link } from 'react-router-dom';

const SpecialistItem = ({specialist}) => {
  return (
    <Paper elevation={3} >
    <Card component={Link} to={`/specialists/${specialist.id}`}>
      <CardActionArea>
        <CardMedia component="img" height="auto" image={specialist.avatar} alt={specialist.email} />
        <CardContent>
          <Typography gutterBottom variant="subtitle1" component="div">
            {`${specialist.first_name} ${specialist.last_name}`}
          </Typography>
          <Box component="p" sx={{ fontWeight: 900 }}>
            {specialist.position}
          </Box>
        </CardContent>
      </CardActionArea>
    </Card>
    </Paper>
  );
};

export default SpecialistItem;
