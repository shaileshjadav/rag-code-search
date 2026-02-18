import {
  Container,
  TextInput,
  Box,
  Image,
  Title,
  Text,
  Loader,
  Button,
  NativeSelect,
} from "@mantine/core";
import { IconSearch } from "@tabler/icons-react";
import useMountedState from "@/hooks/useMountedState";
import { useGetSearchResult } from "@/hooks/useGetSearchResult";
import { getHotkeyHandler, useHotkeys } from "@mantine/hooks";
import { FileTree } from "../FIleTree";
import { CodeContainer } from "../CodeContainer";
import classes from "./Main.module.css";
import { useSearchParams } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";

export default function Main() {
  const [query, setQuery] = useMountedState("");
  const { data, getSearch, loading, error, resetData } = useGetSearchResult();
  const [searchParams, setSearchParams] = useSearchParams();
  const [projectRepo, setProjectRepo] = useState("");

  useHotkeys([
    [
      "/",
      () => {
        const input = document.querySelector("input");
        input?.focus();
      },
    ],
  ]);
  const handleSubmit = () => {
    resetData();
    if (query) {
      getSearch(query, projectRepo);
      setSearchParams({ query });
    }
  };

  useEffect(() => {
    if (query === "") {
      resetData();
    }
  });
  const selectData = useMemo(
    () => [
      { value: "twitter-fullstack", label: "Twitter full stack" },
      { value: "dom-unique-selector", label: "Dom Unique selector" },
    ],
    []
  );

  useEffect(() => {
    // set first item by default
    if (!projectRepo && selectData.length > 0) {
      setProjectRepo(selectData[0].value);
    }
  }, [projectRepo, selectData, setProjectRepo]);

  const select = (
    <>
      <NativeSelect
        data={selectData}
        rightSectionWidth={28}
        required={true}
        value={projectRepo}
        onChange={(event) => setProjectRepo(event.currentTarget.value)}
        withAsterisk
        styles={{
          input: {
            fontWeight: 500,
            borderTopLeftRadius: 0,
            borderBottomLeftRadius: 0,
            width: 200,
            // marginRight: -2,
          },
        }}
      />
      <Button
        radius={4}
        w={"100%"}
        size={"md"}
        variant="filled"
        color="Primary.2"
        onClick={handleSubmit}
      >
        Search
      </Button>
    </>
  );

  return (
    <Container size={"md"}>
      <TextInput
        radius={4}
        size="md"
        placeholder="Enter a query"
        leftSection={<IconSearch color="#102252" />}
        rightSectionWidth={"6rem"}
        value={query}
        pt={data || loading ? "1rem" : "5rem"}
        required
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          setQuery(event.currentTarget.value)
        }
        onKeyDown={getHotkeyHandler([["Enter", handleSubmit]])}
        classNames={{ input: classes.input }}
        rightSection={select}
      />

      {data && (
        <Box
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "flex-start",
            justifyContent: "space-between",
          }}
        >
          <Box className={classes.navbar}>
            <FileTree data={data} />
          </Box>
          <Box pt={"md"} className={classes.codeDisplayArea}>
            {projectRepo &&
              data?.result.map((item) => (
                <CodeContainer
                  {...item}
                  projectRepo={projectRepo}
                  key={`${item.context.snippet} ${item.line_from} ${item.line_to}`}
                />
              ))}
          </Box>
        </Box>
      )}

      {!data && !loading && !error && projectRepo && (
        <>
          <Box
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Image
              src="/landing.gif"
              alt="Landing"
              maw={400}
              h={400}
              fit="contain"
            />
            <Title order={3} className={classes.heading}>
              <span className={classes.headingHighlight}>Code Search with AI</span>
            </Title>
            <Text className={classes.subHeading}>
              Welcome to my code. Get started by entering a query.
            </Text>
            <Text className={classes.subHeading}>
              Instantly understand my GitHub repositories—AI explains the why,
              what, and how.
            </Text>
          </Box>
        </>
      )}
      {loading && (
        <Box className={classes.loader}>
          <Loader type="bars" />
        </Box>
      )}
      {error && (
        <Box>
          <Image src="/error.gif" alt="Error" h={400} fit="contain" />

          <Text className={classes.subHeading}>
            Something went wrong, {error}
          </Text>
        </Box>
      )}
    </Container>
  );
}
