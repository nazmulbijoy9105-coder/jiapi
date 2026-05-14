import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Home from './pages/Home'
import Post2023 from './pages/Post2023'
import Pre2023 from './pages/Pre2023'
import CaseLaw from './pages/CaseLaw'
import Search from './pages/Search'
import DTAA from './pages/DTAA'
import Amendments from './pages/Amendments'
import TaxRates from './pages/TaxRates'
import TPRegulations from './pages/TPRegulations'
import BEPS from './pages/BEPS'
import Compliance from './pages/Compliance'
import APIReference from './pages/APIReference'
import Login from './pages/Login'

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="post2023" element={<Post2023 />} />
          <Route path="pre2023" element={<Pre2023 />} />
          <Route path="caselaw" element={<CaseLaw />} />
          <Route path="search" element={<Search />} />
          <Route path="dtaa" element={<DTAA />} />
          <Route path="amendments" element={<Amendments />} />
          <Route path="tax-rates" element={<TaxRates />} />
          <Route path="tp-regulations" element={<TPRegulations />} />
          <Route path="beps" element={<BEPS />} />
          <Route path="compliance" element={<Compliance />} />
          <Route path="api-reference" element={<APIReference />} />
          <Route path="login" element={<Login />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
