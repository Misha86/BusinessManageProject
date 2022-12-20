import React, { useState, useEffect } from 'react';
import UserService from '../services/user.service';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';
import SpecialistList from '../components/SpecialistList';
import Pagination from '@mui/material/Pagination';
import { Grid, Container } from '@mui/material';
import PageSizeForm from '../components/PageSizeForm';

const Home = () => {
  const [specialists, setSpecialists] = useState([]);
  const [pageSize, setPageSize] = useState(5);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);

  const [fetching, isLoading, error] = useFetching(async (page, pageSize) => {
    const response = await UserService.getSpecialists(page, pageSize);
    setSpecialists(response.data.results);
    setPages(response.data.pages);
  });

  useEffect(() => {
    !!error && setPage(1);
  }, [error]);

  useEffect(() => {
    fetching(page, pageSize);
  }, [page, pageSize, pages]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
        <Container maxWidth="xl">
          <Grid container spacing={3}>
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
                <PageSizeForm setPageSize={setPageSize} pageSize={pageSize} optionArray={[5, 10, 20, 30, 50]} />
              </Grid>
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default Home;
