import React, { useState, useEffect } from 'react';
import UserService from '../services/user.service';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';
import SpecialistList from '../components/SpecialistList';
import Pagination from '@mui/material/Pagination';
import { Grid, Container, Typography, TextField } from '@mui/material';
import SelectForm from '../components/SelectForm';
import Filter from '../components/Filter';
import dayjs from 'dayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Stack from '@mui/material/Stack';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

const Home = () => {
  const [specialists, setSpecialists] = useState([]);
  const [pageSize, setPageSize] = useState(10);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [orderValue, setOrderValue] = useState('');
  const [positionItem, setPositionItem] = useState(null);
  const [dateData, setDateData] = useState(null);

  const [fetching, isLoading, error] = useFetching(async (page, pageSize, orderValue, position, date) => {
    const response = await UserService.getSpecialists(page, pageSize, orderValue, position, date);
    setSpecialists(response.data.results);
    setPages(response.data.pages);
  });

  const pageSizeOptions = [
    [10, 10],
    [20, 20],
    [30, 30],
    [50, 50],
  ];

  const sortByOptions = [
    ['email', 'Email'],
    ['position', 'Position'],
    ['first_name', 'Name'],
  ];

  const positionsOptions = [
    { label: 'Position 1', position: 'position_1' },
    { label: 'Position 2', position: 'position_2' },
    { label: 'Position 3', position: 'position_3' },
  ];

  useEffect(() => {
    !!error && setPage(1);
  }, [error]);

  useEffect(() => {
    const position = positionItem ? positionItem.position : '';
    const stringDate = dateData ? `${dateData?.get('y')}-${dateData?.get('M') + 1}-${dateData?.get('D')}` : '';
    fetching(page, pageSize, orderValue, position, stringDate);
  }, [page, pageSize, pages, orderValue, positionItem, dateData]);

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
        <Container maxWidth="xl">
          <Grid container rowSpacing={2}>
            <Grid item xs display="flex" mt={1} justifyContent="center" alignItems="center">
              <Typography gutterBottom variant="h5" component="h5" color="gray">
                {specialists.length ? 'Specialists' : 'No Specialists yet!!!'}
              </Typography>
            </Grid>

            <Grid container item spacing={2}>
              <Grid item xs={3} sm={2} md={1}>
                <SelectForm setData={setPageSize} defaultValue={pageSize} optionArray={pageSizeOptions} label="Item" />
              </Grid>
              <Grid item xs={4} sm={3} md={2}>
                <SelectForm
                  setData={setOrderValue}
                  defaultValue={orderValue}
                  optionArray={sortByOptions}
                  label="Sort By"
                />
              </Grid>
              <Grid item xs={6} sm={4} md={3}>
                <Filter fields={positionsOptions} setData={setPositionItem} data={positionItem} />
              </Grid>
              <Grid item xs={6} sm={4} md={3}>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <Stack spacing={3}>
                    <DatePicker
                      views={['day']}
                      label="Working date"
                      minDate={dayjs()}
                      maxDate={dayjs().add(45, 'day')}
                      value={dateData}
                      onChange={(newValue) => {
                        setDateData(newValue);
                      }}
                      renderInput={(params) => (
                        <TextField {...params} helperText={params?.inputProps?.placeholder} variant="standard" />
                      )}
                    />
                  </Stack>
                </LocalizationProvider>
              </Grid>
            </Grid>

            <SpecialistList specialists={specialists} />

            <Grid container item rowSpacing={1} mb={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid item xs={12} sm={8} md={5}>
                <Pagination
                  count={pages}
                  variant="outlined"
                  shape="rounded"
                  page={page}
                  onChange={(e, value) => setPage(value)}
                  color="primary"
                />
              </Grid>

              <Grid>
                <SelectForm setData={setPageSize} defaultValue={pageSize} optionArray={pageSizeOptions} label="Item" />
              </Grid>
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default Home;
