import React from 'react';
import { Card, CardActionArea, CardMedia, CardContent, Typography, Box } from '@mui/material';

const SpecialistItem = ({specialist}) => {
  return (
    <Card>
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
  );
};

export default SpecialistItem;
