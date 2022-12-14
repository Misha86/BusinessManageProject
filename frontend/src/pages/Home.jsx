import React, { useState, useEffect, useMemo } from 'react';
import UserService from '../services/user.service';
import useFetching from '../hooks/useFetching';
import useStringDate from '../hooks/useStringDate';
import Loader from '../components/Loader';
import SpecialistList from '../components/SpecialistList';
import Pagination from '@mui/material/Pagination';
import { Grid, Container, Typography } from '@mui/material';
import SelectForm from '../components/SelectForm';
import Filter from '../components/Filter';
import CalendarField from '../components/UI/CalendarField';
import { pageSizeOptions, sortOptions, positionsOptions } from '../utils';

const Home = () => {
  const [specialists, setSpecialists] = useState([]);
  const [pageSize, setPageSize] = useState(10);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [sortValue, setSortValue] = useState('');
  const [positionItem, setPositionItem] = useState(null);
  const [dateData, setDateData] = useState(null);

  const stringDate = useStringDate(dateData);
  const [fetching, isLoading, error] = useFetching(async (page, pageSize, orderValue, position, date) => {
    const response = await UserService.getSpecialists(page, pageSize, orderValue, position, date);
    setSpecialists(response.data.results);
    setPages(response.data.pages);
  });

  useEffect(() => {
    !!error && setPage(1);
  }, [error]);

  const position = useMemo(() => {
    return positionItem ? positionItem.position : '';
  }, [positionItem]);

  useEffect(() => {
      fetching(page, pageSize, sortValue, position, stringDate);
  }, [page, pageSize, sortValue, positionItem, stringDate]);

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
                <SelectForm setData={setPageSize} defaultValue={pageSize} optionArray={pageSizeOptions} label="Items" />
              </Grid>
              <Grid item xs={4} sm={3} md={2}>
                <SelectForm setData={setSortValue} defaultValue={sortValue} optionArray={sortOptions} label="Sort By" />
              </Grid>
              <Grid item xs={6} sm={4} md={3}>
                <Filter fields={positionsOptions} setData={setPositionItem} data={positionItem} />
              </Grid>
              <Grid item xs={6} sm={4} md={3}>
                <CalendarField setDateData={setDateData} dateData={dateData} label="Working date" />
              </Grid>
            </Grid>

            <SpecialistList specialists={specialists} />

            {!!pages && (
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
                  <SelectForm
                    setData={setPageSize}
                    defaultValue={pageSize}
                    optionArray={pageSizeOptions}
                    label="Items"
                  />
                </Grid>
              </Grid>
            )}
          </Grid>
        </Container>
      )}
    </>
  );
};

export default Home;
