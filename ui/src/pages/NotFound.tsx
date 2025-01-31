import React from 'react';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">
        404 - Page Not Found
      </h1>
      <p className="text-gray-600 mb-8">
        Sorry, the page you are looking for does not exist.
      </p>
      <Link
        to="/dashboard"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Go to Dashboard
      </Link>
    </div>
  );
};

export default NotFound;
