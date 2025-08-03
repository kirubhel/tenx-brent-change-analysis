import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Alert, Spinner } from 'react-bootstrap';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [brentData, setBrentData] = useState([]);
  const [eventsData, setEventsData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [selectedDate, setSelectedDate] = useState('2020-03-23'); // COVID-19 start
  const [nearbyEvents, setNearbyEvents] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    if (selectedDate) {
      loadNearbyEvents(selectedDate);
    }
  }, [selectedDate]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load Brent prices
      const brentResponse = await axios.get('/api/data/brent-prices');
      setBrentData(brentResponse.data.data);
      
      // Load events
      const eventsResponse = await axios.get('/api/data/events');
      setEventsData(eventsResponse.data.data);
      
      // Load summary
      const summaryResponse = await axios.get('/api/analysis/summary');
      setSummary(summaryResponse.data);
      
    } catch (err) {
      setError('Failed to load dashboard data. Please check if the backend is running.');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadNearbyEvents = async (date) => {
    try {
      const response = await axios.get(`/api/events/near-date?date=${date}&days=30`);
      setNearbyEvents(response.data.data);
    } catch (err) {
      console.error('Error loading nearby events:', err);
    }
  };

  const formatPrice = (price) => {
    return `$${price.toFixed(2)}`;
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString();
  };

  const getEventColor = (category) => {
    const colors = {
      'Conflict': '#dc3545',
      'Political': '#007bff',
      'Economic': '#28a745',
      'OPEC': '#ffc107',
      'Natural Disaster': '#6f42c1'
    };
    return colors[category] || '#6c757d';
  };

  if (loading) {
    return (
      <Container className="mt-5">
        <Row className="justify-content-center">
          <Col md={6} className="text-center">
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
            <p className="mt-3">Loading Brent Oil Analysis Dashboard...</p>
          </Col>
        </Row>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="mt-5">
        <Alert variant="danger">
          <Alert.Heading>Error</Alert.Heading>
          <p>{error}</p>
          <hr />
          <p className="mb-0">
            Make sure the Flask backend is running on port 5000.
          </p>
        </Alert>
      </Container>
    );
  }

  return (
    <div className="App">
      <Container fluid className="mt-4">
        {/* Header */}
        <Row className="mb-4">
          <Col>
            <h1 className="text-center">Brent Oil Price Change Point Analysis</h1>
            <p className="text-center text-muted">
              Analyzing the impact of major events on oil prices (1987-2022)
            </p>
          </Col>
        </Row>

        {/* Summary Statistics */}
        {summary && (
          <Row className="mb-4">
            <Col md={3}>
              <Card className="text-center">
                <Card.Body>
                  <Card.Title>Total Observations</Card.Title>
                  <Card.Text className="h3">{summary.total_observations.toLocaleString()}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={3}>
              <Card className="text-center">
                <Card.Body>
                  <Card.Title>Average Price</Card.Title>
                  <Card.Text className="h3">{formatPrice(summary.price_statistics.mean)}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={3}>
              <Card className="text-center">
                <Card.Body>
                  <Card.Title>Price Range</Card.Title>
                  <Card.Text className="h6">
                    {formatPrice(summary.price_statistics.min)} - {formatPrice(summary.price_statistics.max)}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={3}>
              <Card className="text-center">
                <Card.Body>
                  <Card.Title>Date Range</Card.Title>
                  <Card.Text className="h6">
                    {formatDate(summary.date_range.start)} - {formatDate(summary.date_range.end)}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        )}

        {/* Main Chart */}
        <Row className="mb-4">
          <Col>
            <Card>
              <Card.Header>
                <h5>Brent Oil Prices Over Time</h5>
              </Card.Header>
              <Card.Body>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={brentData.slice(-1000)}> {/* Show last 1000 points for performance */}
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="date" 
                      tickFormatter={(date) => new Date(date).getFullYear()}
                      interval="equidistant"
                    />
                    <YAxis 
                      domain={['dataMin - 10', 'dataMax + 10']}
                      tickFormatter={(value) => `$${value}`}
                    />
                    <Tooltip 
                      labelFormatter={(date) => formatDate(date)}
                      formatter={(value) => [formatPrice(value), 'Price']}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="price" 
                      stroke="#007bff" 
                      strokeWidth={1}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Events and Analysis */}
        <Row>
          {/* Major Events */}
          <Col md={6}>
            <Card>
              <Card.Header>
                <h5>Major Events Affecting Oil Prices</h5>
              </Card.Header>
              <Card.Body style={{ maxHeight: '400px', overflowY: 'auto' }}>
                {eventsData.slice(0, 10).map((event, index) => (
                  <div key={index} className="mb-3 p-2 border rounded">
                    <div className="d-flex justify-content-between align-items-start">
                      <div>
                        <strong>{event.event}</strong>
                        <br />
                        <small className="text-muted">{formatDate(event.date)}</small>
                        <br />
                        <small>{event.description}</small>
                      </div>
                      <div className="text-end">
                        <span 
                          className="badge" 
                          style={{ backgroundColor: getEventColor(event.category) }}
                        >
                          {event.category}
                        </span>
                        <br />
                        <small className="text-muted">Impact: {event.impact_score}/9</small>
                      </div>
                    </div>
                  </div>
                ))}
              </Card.Body>
            </Card>
          </Col>

          {/* Nearby Events */}
          <Col md={6}>
            <Card>
              <Card.Header>
                <h5>Events Near Selected Date</h5>
                <small className="text-muted">
                  Events within 30 days of {formatDate(selectedDate)}
                </small>
              </Card.Header>
              <Card.Body style={{ maxHeight: '400px', overflowY: 'auto' }}>
                {nearbyEvents.length > 0 ? (
                  nearbyEvents.map((event, index) => (
                    <div key={index} className="mb-3 p-2 border rounded">
                      <div className="d-flex justify-content-between align-items-start">
                        <div>
                          <strong>{event.event}</strong>
                          <br />
                          <small className="text-muted">
                            {formatDate(event.date)} 
                            ({event.days_from_target > 0 ? '+' : ''}{event.days_from_target} days)
                          </small>
                          <br />
                          <small>{event.description}</small>
                        </div>
                        <div className="text-end">
                          <span 
                            className="badge" 
                            style={{ backgroundColor: getEventColor(event.category) }}
                          >
                            {event.category}
                          </span>
                          <br />
                          <small className="text-muted">Impact: {event.impact_score}/9</small>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-muted">No events found within 30 days of the selected date.</p>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Footer */}
        <Row className="mt-4">
          <Col>
            <hr />
            <p className="text-center text-muted">
              Brent Oil Price Change Point Analysis Dashboard | Birhan Energies
            </p>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App; 