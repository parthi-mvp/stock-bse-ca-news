import React, { useState, useEffect } from "react";
import Table, { SelectColumnFilter } from "./Table";

function App() {
  const columns = React.useMemo(
    () => [
      {
        Header: "Company Name",
        accessor: "SLONGNAME",
        Filter: SelectColumnFilter, // new
        Cell: ({ row: { original } }) => (
          <a href={original.NSURL} target="__blank" className="text-blue-700">
            {original.SLONGNAME}
          </a>
        ),
      },
      {
        Header: "NEWSSUB",
        accessor: "NEWSSUB",
      },
      {
        Header: "HEADLINE",
        accessor: "HEADLINE",
        show: false,
      },
      {
        Header: "News Type",
        accessor: "CATEGORYNAME",
        Filter: SelectColumnFilter,
      },
      {
        Header: "PDF",
        accessor: "NSURL",
        Cell: ({ row: { original } }) => (
          <a
            href={
              "https://www.bseindia.com/xml-data/corpfiling/AttachLive/" +
              original.ATTACHMENTNAME
            }
            target="__blank"
            className="py-0.5 px-4 border  leading-wide text-sm rounded-full text-blue-900 hover:bg-blue-200 focus:outline-none  "
          >
            view
          </a>
        ),
      },
      {
        Header: "Date",
        accessor: "date",
        Filter: SelectColumnFilter,
        show: true,
      },
      {
        Header: "NEWS_DT",
        accessor: "NEWS_DT",
        show: false,
      },
      {
        Header: "Company ID",
        accessor: "SCRIP_CD",
        show: false,
      },
      {
        Header: "News ID",
        accessor: "NEWSID",
        show: false,
      },
      {
        Header: "DissemDT",
        accessor: "DissemDT",
        show: false,
      },
      {
        Header: "News_submission_dt",
        accessor: "News_submission_dt",
        show: false,
      },
    ],
    []
  );

  const [state, setState] = useState([]);
  const date = new Date();
  function get_data() {
    return fetch("http://127.0.0.1:5000/bse/news/data")
      .then((res) => res.json())
      .then((data) => setState(data));
  }
  useEffect(() => {
    get_data();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 text-sm">
      <main className="p-10">
        <div className="flex flex-col">
          <h1 className=" text-3xl font-semibold text-center flex-1">
            BSE India Corporate Announcements
          </h1>
          <h3 className="text-center pt-2">
            Lasted updated at {date.toDateString()}
          </h3>
        </div>
        <div className="mt-12">
          <Table columns={columns} data={state} />
        </div>
      </main>
    </div>
  );
}

export default App;
