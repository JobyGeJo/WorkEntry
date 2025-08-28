import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

export default function Layout({ user, setUser }) {
  return (
    <>
      <Navbar user={user} setUser={setUser} />
      <main>
        <Outlet />
      </main>
    </>
  );
}