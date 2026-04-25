import { useState, useEffect } from 'react';

function App() {
  const [stops, setStops] = useState([]);
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [loading, setLoading] = useState(false);
  const [mapHtml, setMapHtml] = useState(null);
  const [showMap, setShowMap] = useState(false);
  const [routeInfo, setRouteInfo] = useState(null);
  const [error, setError] = useState(null);
  const [recentSearches, setRecentSearches] = useState([]);
  const [searchQuery, setSearchQuery] = useState({ from: '', to: '' });

  // Fetch stops from backend
  useEffect(() => {
    fetchStops();
    loadRecentSearches();
  }, []);

  const fetchStops = async () => {
    try {
      const response = await fetch('http://localhost:8000/stops');
      const data = await response.json();
      
      let stopsArray = [];
      if (Array.isArray(data)) {
        stopsArray = data.map(stop => ({
          id: stop.id,
          name: stop.id,
          lat: stop.lat,
          lng: stop.lon
        }));
      }
      
      setStops(stopsArray);
    } catch (err) {
      console.error('Error fetching stops:', err);
      setError('Failed to connect to backend. Make sure server is running.');
    }
  };

  const loadRecentSearches = () => {
    const saved = localStorage.getItem('recentSearches');
    if (saved) {
      setRecentSearches(JSON.parse(saved));
    }
  };

  const saveRecentSearch = (origin, destination) => {
    const newSearch = { origin, destination, timestamp: Date.now() };
    const updated = [newSearch, ...recentSearches.filter(s => 
      !(s.origin === origin && s.destination === destination)
    )].slice(0, 5);
    setRecentSearches(updated);
    localStorage.setItem('recentSearches', JSON.stringify(updated));
  };

  const findRoute = async () => {
    if (!origin || !destination) return;
    
    setLoading(true);
    setError(null);
    setShowMap(false);
    setRouteInfo(null);
    
    const encodedOrigin = encodeURIComponent(origin);
    const encodedDestination = encodeURIComponent(destination);
    
    try {
      const routeResponse = await fetch(
        `http://localhost:8000/route?origin=${encodedOrigin}&destination=${encodedDestination}`
      );
      
      if (!routeResponse.ok) {
        throw new Error(`Route not found (${routeResponse.status})`);
      }
      
      const routeData = await routeResponse.json();
      
      const optimal = routeData.optimal_route;
      const naive = routeData.naive_route;
      
      if (!optimal || !optimal.path) {
        throw new Error('No route found between these stops');
      }
      
      const optimalTime = optimal?.total_time || 0;
      const naiveTime = naive?.total_time || 0;
      const timeSaved = Math.abs(naiveTime - optimalTime);
      const savingsPercent = naiveTime > 0 ? Math.round((naiveTime - optimalTime) / naiveTime * 100) : 0;
      
      setRouteInfo({
        optimal: {
          path: optimal?.path || [],
          time: optimalTime,
          transfers: optimal?.transfers || 0,
          waitTime: optimal?.wait_time || 0,
          travelTime: optimal?.travel_time || optimalTime
        },
        naive: {
          path: naive?.path || [],
          time: naiveTime,
          transfers: naive?.transfers || 0
        },
        timeSaved: Math.abs(timeSaved),
        savingsPercent: Math.abs(savingsPercent),
        isOptimalBetter: optimalTime < naiveTime
      });
      
      const mapResponse = await fetch('http://localhost:8002/api/map-html', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origin, destination })
      });
      
      if (mapResponse.ok) {
        const html = await mapResponse.text();
        setMapHtml(html);
        setShowMap(true);
        saveRecentSearch(origin, destination);
      } else {
        throw new Error('Map generation failed');
      }
      
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'Failed to find route. Make sure both servers are running.');
    }
    
    setLoading(false);
  };

  const swapLocations = () => {
    setOrigin(destination);
    setDestination(origin);
    setSearchQuery({ from: destination, to: origin });
  };

  const useCurrentLocation = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        let nearest = null;
        let minDist = Infinity;
        stops.forEach(stop => {
          const dist = Math.hypot(
            stop.lat - position.coords.latitude,
            stop.lng - position.coords.longitude
          );
          if (dist < minDist) {
            minDist = dist;
            nearest = stop;
          }
        });
        if (nearest) {
          setOrigin(nearest.name);
        }
      }, (error) => {
        console.error('Geolocation error:', error);
        setError('Could not get your location. Please allow location access.');
      });
    } else {
      setError('Geolocation is not supported by your browser');
    }
  };

  const filteredStops = (type) => {
    const query = type === 'from' ? searchQuery.from : searchQuery.to;
    if (!query) return stops;
    return stops.filter(stop => 
      stop.name.toLowerCase().includes(query.toLowerCase())
    );
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <div>
            <h1 style={styles.title}>
              <span style={styles.titleIcon}>🚌</span>
              Kathmandu Transport Optimizer
            </h1>
            <p style={styles.subtitle}>
              Intelligent route planning using Dijkstra's algorithm | Real road routing | SDG 11.2
            </p>
          </div>
          <div style={styles.badge}>
            <span style={styles.badgeIcon}>⚡</span>
            <span>AI-Powered Routes</span>
          </div>
        </div>
      </header>
      
      {/* Search Panel */}
      <div style={styles.searchPanel}>
        <div style={styles.searchContainer}>
          {/* Origin */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <span style={styles.labelIcon}>📍</span> From
            </label>
            <div style={styles.selectWrapper}>
              <select 
                value={origin} 
                onChange={(e) => setOrigin(e.target.value)}
                style={styles.select}
              >
                <option value="">Select starting point</option>
                {stops.map((stop) => (
                  <option key={stop.id} value={stop.name}>
                    {stop.name}
                  </option>
                ))}
              </select>
              <button onClick={useCurrentLocation} style={styles.locationBtn} title="Use my current location">
                🎯
              </button>
            </div>
          </div>
          
          {/* Swap Button */}
          <button onClick={swapLocations} style={styles.swapBtn} title="Swap locations">
            <span style={styles.swapIcon}>↕️</span>
          </button>
          
          {/* Destination */}
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <span style={styles.labelIcon}>🎯</span> To
            </label>
            <select 
              value={destination} 
              onChange={(e) => setDestination(e.target.value)}
              style={styles.select}
            >
              <option value="">Select destination</option>
              {stops.map((stop) => (
                <option key={stop.id} value={stop.name}>
                  {stop.name}
                </option>
              ))}
            </select>
          </div>
          
          {/* Find Button */}
          <button 
            onClick={findRoute}
            disabled={!origin || !destination || loading}
            style={{
              ...styles.findBtn,
              ...((!origin || !destination || loading) ? styles.findBtnDisabled : {})
            }}
          >
            {loading ? (
              <span style={styles.loadingSpinner}>
                <span style={styles.spinner}></span>
                Computing...
              </span>
            ) : (
              <span>🔍 Find Route</span>
            )}
          </button>
        </div>
        
        {/* Recent Searches */}
        {recentSearches.length > 0 && !showMap && (
          <div style={styles.recentContainer}>
            <span style={styles.recentLabel}>📌 Recent:</span>
            {recentSearches.map((search, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setOrigin(search.origin);
                  setDestination(search.destination);
                }}
                style={styles.recentBtn}
              >
                {search.origin.length > 15 ? search.origin.substring(0, 15) + '...' : search.origin} → 
                {search.destination.length > 15 ? search.destination.substring(0, 15) + '...' : search.destination}
              </button>
            ))}
          </div>
        )}
      </div>
      
      {/* Error Message */}
      {error && (
        <div style={styles.errorContainer}>
          <div style={styles.errorIcon}>⚠️</div>
          <div style={styles.errorContent}>
            <div style={styles.errorTitle}>Route Error</div>
            <div style={styles.errorMessage}>{error}</div>
          </div>
          <button onClick={() => setError(null)} style={styles.errorClose}>✕</button>
        </div>
      )}
      
      {/* Route Info Summary */}
      {routeInfo && !showMap && (
        <div style={styles.summaryContainer}>
          <div style={styles.summaryHeader}>
            <span style={styles.summaryIcon}>✅</span>
            <span style={styles.summaryTitle}>Route Analysis</span>
          </div>
          
          <div style={styles.summaryGrid}>
            <div style={styles.summaryCard}>
              <div style={styles.summaryCardIcon}>🚀</div>
              <div style={styles.summaryCardTitle}>Optimal Route (Dijkstra)</div>
              <div style={styles.summaryCardValue}>{routeInfo.optimal.time} <span style={styles.summaryCardUnit}>min</span></div>
              <div style={styles.summaryCardSub}>{routeInfo.optimal.transfers} transfers</div>
            </div>
            
            <div style={styles.summaryCard}>
              <div style={styles.summaryCardIcon}>🐢</div>
              <div style={styles.summaryCardTitle}>Naive Route</div>
              <div style={styles.summaryCardValue}>{routeInfo.naive.time} <span style={styles.summaryCardUnit}>min</span></div>
              <div style={styles.summaryCardSub}>{routeInfo.naive.transfers} transfers</div>
            </div>
            
            <div style={{...styles.summaryCard, background: 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)'}}>
              <div style={styles.summaryCardIcon}>⏱️</div>
              <div style={styles.summaryCardTitle}>Time Saved</div>
              <div style={{...styles.summaryCardValue, color: '#2e7d32'}}>
                {routeInfo.timeSaved} <span style={styles.summaryCardUnit}>min</span>
              </div>
              <div style={styles.summaryCardSub}>
                {routeInfo.savingsPercent}% faster than naive
              </div>
            </div>
          </div>
          
          <div style={styles.summaryPath}>
            <div style={styles.summaryPathLabel}>🗺️ Optimal Path</div>
            <div style={styles.summaryPathContent}>
              {routeInfo.optimal.path.map((stop, idx) => (
                <span key={idx}>
                  <span style={styles.pathStop}>{stop}</span>
                  {idx < routeInfo.optimal.path.length - 1 && <span style={styles.pathArrow}> → </span>}
                </span>
              ))}
            </div>
          </div>
          
          <button onClick={() => setShowMap(true)} style={styles.viewMapBtn}>
            🗺️ View on Map
          </button>
        </div>
      )}
      
      {/* Map Display */}
      {showMap && mapHtml && (
        <div style={styles.mapContainer}>
          <iframe
            srcDoc={mapHtml}
            style={styles.iframe}
            title="Route Map"
          />
          <div style={styles.mapControls}>
            <button onClick={() => setShowMap(false)} style={styles.closeMapBtn}>
              ✕ Back to Search
            </button>
            {routeInfo && (
              <div style={styles.mapInfo}>
                <span style={styles.mapInfoText}>
                  🟢 Optimal: {routeInfo.optimal.time} min | 
                  ⚪ Naive: {routeInfo.naive.time} min | 
                  💚 Save: {routeInfo.timeSaved} min
                </span>
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Placeholder */}
      {!showMap && !routeInfo && (
        <div style={styles.placeholder}>
          <div style={styles.placeholderContent}>
            <div style={styles.placeholderIcon}>🗺️</div>
            <h3 style={styles.placeholderTitle}>Find Your Optimal Route</h3>
            <p style={styles.placeholderText}>
              Select your starting point and destination to see the most efficient path
              using Dijkstra's algorithm on Kathmandu's bus network.
            </p>
            <div style={styles.features}>
              <div style={styles.featureItem}>
                <span style={styles.featureIcon}>🚌</span>
                <span>114+ Stops</span>
              </div>
              <div style={styles.featureItem}>
                <span style={styles.featureIcon}>⚡</span>
                <span>Dijkstra Algorithm</span>
              </div>
              <div style={styles.featureItem}>
                <span style={styles.featureIcon}>🛣️</span>
                <span>Real Roads</span>
              </div>
              <div style={styles.featureItem}>
                <span style={styles.featureIcon}>📱</span>
                <span>Mobile Ready</span>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Status Bar */}
      <div style={styles.statusBar}>
        <span style={{...styles.statusDot, background: stops.length > 0 ? '#10b981' : '#f59e0b'}}></span>
        <span>{stops.length > 0 ? `${stops.length} stops available` : 'Connecting to server...'}</span>
      </div>
    </div>
  );
}

// Professional Styles
const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#f0f2f5',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif',
  },
  header: {
    background: 'linear-gradient(135deg, #0f766e 0%, #0d9488 50%, #14b8a6 100%)',
    color: 'white',
    padding: '20px 32px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  headerContent: {
    maxWidth: '1400px',
    margin: '0 auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '16px',
  },
  title: {
    fontSize: '28px',
    fontWeight: '700',
    margin: 0,
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    letterSpacing: '-0.5px',
  },
  titleIcon: {
    fontSize: '32px',
  },
  subtitle: {
    fontSize: '13px',
    opacity: 0.85,
    marginTop: '6px',
    letterSpacing: '0.3px',
  },
  badge: {
    background: 'rgba(255,255,255,0.2)',
    backdropFilter: 'blur(10px)',
    padding: '8px 16px',
    borderRadius: '40px',
    fontSize: '13px',
    fontWeight: '500',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  badgeIcon: {
    fontSize: '14px',
  },
  searchPanel: {
    background: 'white',
    padding: '20px 32px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
    borderBottom: '1px solid #e9ecef',
  },
  searchContainer: {
    maxWidth: '1400px',
    margin: '0 auto',
    display: 'flex',
    gap: '20px',
    alignItems: 'flex-end',
    flexWrap: 'wrap',
  },
  inputGroup: {
    flex: 2,
    minWidth: '220px',
  },
  label: {
    display: 'block',
    fontSize: '13px',
    fontWeight: '600',
    color: '#34495e',
    marginBottom: '8px',
    letterSpacing: '0.3px',
  },
  labelIcon: {
    marginRight: '6px',
  },
  selectWrapper: {
    display: 'flex',
    gap: '10px',
    position: 'relative',
  },
  select: {
    width: '100%',
    padding: '12px 14px',
    border: '2px solid #e2e8f0',
    borderRadius: '12px',
    fontSize: '14px',
    fontWeight: '500',
    background: 'white',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    outline: 'none',
  },
  locationBtn: {
    padding: '0 18px',
    background: '#f1f5f9',
    border: '2px solid #e2e8f0',
    borderRadius: '12px',
    cursor: 'pointer',
    fontSize: '18px',
    transition: 'all 0.2s ease',
    fontWeight: '500',
  },
  swapBtn: {
    padding: '12px 18px',
    background: '#f1f5f9',
    border: '2px solid #e2e8f0',
    borderRadius: '12px',
    cursor: 'pointer',
    fontSize: '18px',
    transition: 'all 0.2s ease',
    marginBottom: '0px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  swapIcon: {
    display: 'inline-block',
  },
  findBtn: {
    padding: '12px 32px',
    background: 'linear-gradient(135deg, #0f766e 0%, #0d9488 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    minWidth: '160px',
    boxShadow: '0 2px 8px rgba(13,148,136,0.3)',
  },
  findBtnDisabled: {
    opacity: 0.5,
    cursor: 'not-allowed',
    boxShadow: 'none',
  },
  loadingSpinner: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
  },
  spinner: {
    width: '18px',
    height: '18px',
    border: '2px solid white',
    borderTop: '2px solid transparent',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  recentContainer: {
    maxWidth: '1400px',
    margin: '16px auto 0',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    flexWrap: 'wrap',
  },
  recentLabel: {
    fontSize: '12px',
    fontWeight: '500',
    color: '#64748b',
  },
  recentBtn: {
    padding: '5px 12px',
    background: '#f1f5f9',
    border: '1px solid #e2e8f0',
    borderRadius: '20px',
    fontSize: '11px',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.15s ease',
    color: '#475569',
  },
  errorContainer: {
    position: 'fixed',
    top: '120px',
    left: '50%',
    transform: 'translateX(-50%)',
    background: '#fef2f2',
    border: '1px solid #fecaca',
    borderRadius: '16px',
    padding: '12px 20px',
    display: 'flex',
    alignItems: 'center',
    gap: '14px',
    zIndex: 1000,
    boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
    maxWidth: '90%',
  },
  errorIcon: {
    fontSize: '22px',
  },
  errorContent: {
    flex: 1,
  },
  errorTitle: {
    fontWeight: '700',
    color: '#dc2626',
    fontSize: '13px',
  },
  errorMessage: {
    fontSize: '12px',
    color: '#b91c1c',
  },
  errorClose: {
    background: 'none',
    border: 'none',
    fontSize: '20px',
    cursor: 'pointer',
    color: '#dc2626',
    padding: '0 6px',
    fontWeight: 'bold',
  },
  summaryContainer: {
    maxWidth: '1100px',
    margin: '24px auto',
    padding: '0 32px',
    width: '100%',
  },
  summaryHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '20px',
  },
  summaryIcon: {
    fontSize: '24px',
  },
  summaryTitle: {
    fontSize: '20px',
    fontWeight: '700',
    color: '#1e293b',
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '20px',
    marginBottom: '24px',
  },
  summaryCard: {
    background: 'white',
    borderRadius: '20px',
    padding: '20px',
    textAlign: 'center',
    border: '1px solid #e2e8f0',
    boxShadow: '0 4px 12px rgba(0,0,0,0.04)',
    transition: 'transform 0.2s ease',
  },
  summaryCardIcon: {
    fontSize: '28px',
    marginBottom: '8px',
  },
  summaryCardTitle: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    marginBottom: '12px',
  },
  summaryCardValue: {
    fontSize: '36px',
    fontWeight: '800',
    color: '#0d9488',
    lineHeight: '1.2',
  },
  summaryCardUnit: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#94a3b8',
  },
  summaryCardSub: {
    fontSize: '11px',
    color: '#94a3b8',
    marginTop: '8px',
  },
  summaryPath: {
    background: '#f8fafc',
    borderRadius: '16px',
    padding: '18px 20px',
    border: '1px solid #e2e8f0',
    marginBottom: '20px',
  },
  summaryPathLabel: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#64748b',
    marginBottom: '12px',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  summaryPathContent: {
    fontSize: '14px',
    color: '#1e293b',
    wordBreak: 'break-all',
    lineHeight: '1.6',
  },
  pathStop: {
    background: '#e2e8f0',
    padding: '4px 10px',
    borderRadius: '20px',
    display: 'inline-block',
    margin: '2px 0',
    fontSize: '12px',
    fontWeight: '500',
  },
  pathArrow: {
    color: '#94a3b8',
    margin: '0 6px',
  },
  viewMapBtn: {
    width: '100%',
    padding: '14px',
    background: 'linear-gradient(135deg, #0f766e 0%, #0d9488 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '16px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  mapContainer: {
    flex: 1,
    position: 'relative',
  },
  iframe: {
    width: '100%',
    height: '100%',
    border: 'none',
  },
  mapControls: {
    position: 'absolute',
    top: '20px',
    left: '20px',
    right: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '12px',
    zIndex: 100,
  },
  closeMapBtn: {
    background: 'white',
    border: '1px solid #e2e8f0',
    borderRadius: '40px',
    padding: '10px 20px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    transition: 'all 0.2s ease',
    color: '#1e293b',
  },
  mapInfo: {
    background: 'rgba(0,0,0,0.75)',
    backdropFilter: 'blur(10px)',
    borderRadius: '40px',
    padding: '8px 18px',
  },
  mapInfoText: {
    fontSize: '12px',
    color: 'white',
    fontWeight: '500',
  },
  placeholder: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
  },
  placeholderContent: {
    textAlign: 'center',
    padding: '40px',
    maxWidth: '500px',
  },
  placeholderIcon: {
    fontSize: '80px',
    marginBottom: '24px',
  },
  placeholderTitle: {
    fontSize: '28px',
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: '12px',
  },
  placeholderText: {
    fontSize: '15px',
    color: '#64748b',
    marginBottom: '32px',
    lineHeight: '1.5',
  },
  features: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '16px',
    justifyContent: 'center',
  },
  featureItem: {
    background: 'white',
    padding: '10px 20px',
    borderRadius: '40px',
    fontSize: '13px',
    fontWeight: '600',
    color: '#0d9488',
    border: '1px solid #cbd5e1',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  featureIcon: {
    fontSize: '16px',
  },
  statusBar: {
    position: 'fixed',
    bottom: '16px',
    right: '16px',
    background: 'rgba(0,0,0,0.8)',
    backdropFilter: 'blur(10px)',
    color: 'white',
    fontSize: '11px',
    fontWeight: '500',
    padding: '8px 16px',
    borderRadius: '40px',
    zIndex: 100,
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    letterSpacing: '0.3px',
  },
  statusDot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    animation: 'pulse 2s infinite',
  },
};

// Add animations
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  select:hover {
    border-color: #0d9488;
  }
  button:active {
    transform: translateY(0);
  }
`;
document.head.appendChild(styleSheet);

export default App;