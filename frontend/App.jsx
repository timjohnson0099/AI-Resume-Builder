import React, { useState } from 'react';
import './autofill-fix.css';
import './glow-bg.css';
import './glass-input.css';
import './theme-scrollbar.css';
import './mui-input-theme-fix.css';
import { Container, TextField, Button, Typography, Box, Paper, CircularProgress, Snackbar, Alert, Chip, Divider, Stack, Card, CardContent } from '@mui/material';

const API_URL = 'http://localhost:5000';




function App() {
  const [form, setForm] = useState({ name: '', email: '', phone: '', raw_text: '' });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error('Failed to generate resume');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setResult(null);
    setShowForm(false);
  };

  const download = (type) => {
    if (!result) return;
    const url = `${API_URL}/download/${type}?temp_dir=${result.temp_dir}`;
    window.open(url, '_blank');
  };

  // Helper to render experience block
  const renderExperience = (experience) => (
    <Stack spacing={3}>
      {experience.map((exp, idx) => (
        <Card key={idx} variant="outlined" sx={{ bgcolor: 'rgba(44,24,64,0.92)', color: '#fff', border: '1px solid #6a3093', borderRadius: 3, boxShadow: '0 2px 12px #0004' }}>
          <CardContent>
            <Typography variant="subtitle1" fontWeight={700} sx={{ color: '#a044ff', fontSize: 20 }}>{exp.role} <span style={{ color: '#fff', fontWeight: 500 }}>@ {exp.company}</span></Typography>
            <Typography variant="body2" sx={{ mb: 1, color: '#bbaaff', fontWeight: 500 }}>
              {exp.start_date} - {exp.end_date || 'Present'}
            </Typography>
            <Typography variant="body1" sx={{ color: '#e0e0ff', fontSize: 16 }}>{exp.description}</Typography>
          </CardContent>
        </Card>
      ))}
    </Stack>
  );

  // No longer using gradientBg, replaced by animated glowing background

  return (
    <>
      <div className="animated-bg"><div className="glow"></div></div>
      <Container maxWidth="md" sx={{ py: 4, minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative', color: '#f3f3fa' }}>
        {!showForm && !result && (
          <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="80vh" width={1}>
            <Typography variant="h2" align="center" fontWeight={800} color="#fff" sx={{ mb: 2, textShadow: '0 2px 16px #0008', letterSpacing: 1 }}>
              AI Resume Builder
            </Typography>
            <Typography variant="h6" align="center" color="#e0e0e0" sx={{ mb: 4, maxWidth: 600, textShadow: '0 1px 8px #0006', fontWeight: 400 }}>
              Create a tailored resume containing all the right keywords, improve your writing & highlight your strengths. Powered by AI.
            </Typography>
            <Button
              size="large"
              sx={{
                fontWeight: 700,
                fontSize: 22,
                px: 5,
                py: 2,
                borderRadius: 4,
                boxShadow: '0 4px 24px #0004',
                background: 'linear-gradient(90deg, #a044ff 0%, #6a3093 100%)',
                color: '#fff',
                letterSpacing: 1,
                '&:hover': {
                  background: 'linear-gradient(90deg, #6a3093 0%, #a044ff 100%)',
                },
              }}
              onClick={() => setShowForm(true)}
            >
              Build your resume with AI
            </Button>
          </Box>
        )}
        {showForm && !result && (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh" width={1}>
            <Paper sx={{
              p: { xs: 2, sm: 4 },
              width: 1,
              maxWidth: 900,
              color: '#fff',
              borderRadius: 4,
              display: 'flex',
              justifyContent: 'center',
              background: 'rgba(30, 18, 54, 0.45)',
              boxShadow: '0 8px 40px 0 rgba(80,40,180,0.18), 0 1.5px 8px 0 #0008',
              backdropFilter: 'blur(18px) saturate(160%)',
              WebkitBackdropFilter: 'blur(18px) saturate(160%)',
              border: '1.5px solid rgba(160,68,255,0.18)',
            }} elevation={0}>
              <form onSubmit={handleSubmit} style={{ width: '100%' }}>
                <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={4} width={1}>
                  <Box flex={1} display="flex" flexDirection="column" gap={3} className="glass-input">
                    <TextField label="Name" name="name" value={form.name} onChange={handleChange} required InputLabelProps={{ style: { color: '#bbaaff' } }} />
                    <TextField label="Email" name="email" value={form.email} onChange={handleChange} required type="email" InputLabelProps={{ style: { color: '#bbaaff' } }} />
                    <TextField label="Phone" name="phone" value={form.phone} onChange={handleChange} InputLabelProps={{ style: { color: '#bbaaff' } }} />
                  </Box>
                  <Box flex={2} display="flex" flexDirection="column" gap={3} className="glass-input">
                    <TextField label="Skills & Experience (free text)" name="raw_text" value={form.raw_text} onChange={handleChange} required multiline minRows={6} InputLabelProps={{ style: { color: '#bbaaff' } }} sx={{ borderRadius: 2, maxHeight: 260, overflow: 'auto' }} InputProps={{ className: 'theme-scrollbar' }} />
                    <Button
                      type="submit"
                      size="large"
                      disabled={loading}
                      sx={{
                        fontWeight: 700,
                        fontSize: 18,
                        px: 3,
                        py: 1.5,
                        borderRadius: 3,
                        background: 'linear-gradient(90deg, #a044ff 0%, #6a3093 100%)',
                        color: '#fff',
                        letterSpacing: 1,
                        alignSelf: 'flex-end',
                        '&:hover': {
                          background: 'linear-gradient(90deg, #6a3093 0%, #a044ff 100%)',
                        },
                      }}
                    >
                      {loading ? <CircularProgress size={24} sx={{ color: '#fff' }} /> : 'Generate Resume'}
                    </Button>
                  </Box>
                </Box>
              </form>
            </Paper>
          </Box>
        )}
        {result && (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh" width={1}>
            <Paper sx={{
              p: { xs: 2, sm: 4 },
              width: 1,
              maxWidth: 900,
              color: '#fff',
              borderRadius: 4,
              background: 'rgba(30, 18, 54, 0.45)',
              boxShadow: '0 8px 40px 0 rgba(80,40,180,0.18), 0 1.5px 8px 0 #0008',
              backdropFilter: 'blur(18px) saturate(160%)',
              WebkitBackdropFilter: 'blur(18px) saturate(160%)',
              border: '1.5px solid rgba(160,68,255,0.18)',
            }} elevation={0}>
              <Button onClick={handleBack} variant="outlined" sx={{ mb: 2, color: '#a044ff', borderColor: '#a044ff', fontWeight: 700, letterSpacing: 1, '&:hover': { borderColor: '#6a3093', color: '#fff', background: 'linear-gradient(90deg, #6a3093 0%, #a044ff 100%)' } }}>&larr; BACK</Button>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 700, letterSpacing: 1 }}>Summary</Typography>
              <Typography variant="body1" sx={{ mb: 2, color: '#e0e0ff', fontSize: 18, lineHeight: 1.6 }}>{result.resume_json.summary}</Typography>
              <Divider sx={{ my: 2, borderColor: '#444' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>Skills</Typography>
              <Box sx={{ mb: 2, maxHeight: 120, overflow: 'auto' }} className="theme-scrollbar">
                {result.resume_json.skills && result.resume_json.skills.length > 0 ? (
                  <Box sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'center',
                    gap: 2,
                    rowGap: 2,
                    columnGap: 2,
                    maxWidth: 800,
                    mx: 'auto',
                  }}>
                    {result.resume_json.skills.map((skill, idx) => (
                      <Chip key={idx} label={skill} sx={{
                        bgcolor: 'rgba(160,68,255,0.18)',
                        color: '#fff',
                        fontWeight: 600,
                        fontSize: 16,
                        px: 2,
                        py: 1,
                        mb: 1,
                        borderRadius: 2,
                        border: '1px solid #a044ff',
                        boxShadow: '0 1px 6px #6a309355',
                        letterSpacing: 0.5,
                      }} />
                    ))}
                  </Box>
                ) : (
                  <Typography variant="body2" color="#bbb">No skills listed.</Typography>
                )}
              </Box>
              <Divider sx={{ my: 2, borderColor: '#444' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>Experience</Typography>
              <Box
                className="theme-scrollbar"
                sx={{
                  mb: 2,
                  maxHeight: 320,
                  overflow: 'auto',
                  pr: 1,
                }}
              >
                {result.resume_json.experience && result.resume_json.experience.length > 0 ? (
                  renderExperience(result.resume_json.experience)
                ) : (
                  <Typography variant="body2" color="#bbb">No experience listed.</Typography>
                )}
              </Box>
              <Divider sx={{ my: 2, borderColor: '#444' }} />
              <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  sx={{
                    background: 'linear-gradient(90deg, #a044ff 0%, #6a3093 100%)',
                    color: '#fff',
                    fontWeight: 700,
                    px: 3,
                    py: 1.5,
                    borderRadius: 3,
                    letterSpacing: 1,
                    fontSize: 18,
                    '&:hover': {
                      background: 'linear-gradient(90deg, #6a3093 0%, #a044ff 100%)',
                    },
                  }}
                  onClick={() => download('pdf')}
                >
                  Download PDF
                </Button>
                <Button variant="outlined" sx={{ color: '#a044ff', borderColor: '#a044ff', fontWeight: 700, letterSpacing: 1, fontSize: 18, '&:hover': { borderColor: '#6a3093', color: '#fff', background: 'linear-gradient(90deg, #6a3093 0%, #a044ff 100%)' } }} onClick={() => download('md')}>Download Markdown</Button>
                <Button variant="outlined" sx={{ color: '#a044ff', borderColor: '#a044ff', fontWeight: 700, letterSpacing: 1, fontSize: 18, '&:hover': { borderColor: '#6a3093', color: '#fff', background: 'linear-gradient(90deg, #6a3093 0%, #a044ff 100%)' } }} onClick={() => download('json')}>Download JSON</Button>
              </Box>
            </Paper>
          </Box>
        )}
        <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError('')}>
          <Alert severity="error" onClose={() => setError('')}>{error}</Alert>
        </Snackbar>
      </Container>
    </>
  );
}

export default App;
