import React, { useState, useEffect } from 'react';
import UserService from '../services/user.service';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';
import SpecialistList from '../components/SpecialistList';
import Pagination from '@mui/material/Pagination';
import { Grid, Container, Typography } from '@mui/material';
import SelectForm from '../components/SelectForm';

const Home = () => {
  const [specialists, setSpecialists] = useState([]);
  const [pageSize, setPageSize] = useState(10);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [orderValue, setOrderValue] = useState('');

  const [fetching, isLoading, error] = useFetching(async (page, pageSize, orderValue) => {
    const response = await UserService.getSpecialists(page, pageSize, orderValue);
    setSpecialists(response.data.results);
    setPages(response.data.pages);
  });

  useEffect(() => {
    !!error && setPage(1);
  }, [error]);

  useEffect(() => {
    fetching(page, pageSize, orderValue);
  }, [page, pageSize, pages, orderValue]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const handlePageSize = (event) => {
    setPageSize(event.target.value);
  };

  const handleOrderValue = (event) => {
    setOrderValue(event.target.value);
  };

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
                <SelectForm
                  handler={handlePageSize}
                  defaultValue={pageSize}
                  optionArray={[
                    [10, 10],
                    [20, 20],
                    [30, 30],
                    [50, 50],
                  ]}
                  label="Item"
                />
              </Grid>
              <Grid item xs={4} sm={3} md={2}>
                <SelectForm
                  handler={handleOrderValue}
                  defaultValue={orderValue}
                  optionArray={[
                    ['email', 'Email'],
                    ['position', 'Position'],
                    ['first_name', 'Name'],
                  ]}
                  label="Sort By"
                />
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
                  onChange={handlePageChange}
                  color="primary"
                />
              </Grid>

              <Grid>
                <SelectForm
                  handler={handlePageSize}
                  defaultValue={pageSize}
                  optionArray={[
                    [10, 10],
                    [20, 20],
                    [30, 30],
                    [50, 50],
                  ]}
                  label="Item"
                />
              </Grid>
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default Home;
