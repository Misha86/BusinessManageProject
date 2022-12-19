import React, { useState, useEffect } from 'react';
import UserService from '../services/user.service';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';
import SpecialistList from '../components/SpecialistList';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import { Grid, Container, Typography } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import NativeSelect from '@mui/material/NativeSelect';

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

  // if (Object.keys(error).length !==  0) {
  //   console.log(error);
  //   setPage(1);
  // }

  useEffect(() => {
    fetching(page, pageSize);
  }, [page, pageSize, pages]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const handlePageSize = (event) => {
    setPageSize(event.target.value);
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
                <FormControl fullWidth onChange={handlePageSize}>
                  <InputLabel variant="standard" htmlFor="uncontrolled-native" onChange={handlePageSize}>
                    Items
                  </InputLabel>
                  <NativeSelect
                    defaultValue={pageSize}
                    inputProps={{
                      name: 'items',
                      id: 'uncontrolled-native',
                    }}
                  >
                    <option value={5}>5</option>
                    <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={30}>30</option>
                    <option value={50}>50</option>
                  </NativeSelect>
                </FormControl>
              </Grid>
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default Home;
