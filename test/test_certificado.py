import unittest
from unittest.mock import patch
from io import BytesIO
import os
from app import create_app


class CertificadoEndpointsTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.services.AlumnoService.generar_certificado_alumno_regular')
    def test_certificado_pdf(self, mock_gen):
        mock_gen.return_value = BytesIO(b"%PDF-1.4\n%dummy")
        resp = self.client.get('/api/v1/certificado/1/pdf')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/pdf')

    @patch('app.services.AlumnoService.generar_certificado_alumno_regular')
    def test_certificado_odt(self, mock_gen):
        mock_gen.return_value = BytesIO(b"ODT-DUMMY")
        resp = self.client.get('/api/v1/certificado/1/odt')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/vnd.oasis.opendocument.text', resp.headers.get('Content-Type', ''))
        # as_attachment=True should set Content-Disposition
        self.assertIn('attachment', resp.headers.get('Content-Disposition', ''))

    @patch('app.services.AlumnoService.generar_certificado_alumno_regular')
    def test_certificado_docx(self, mock_gen):
        mock_gen.return_value = BytesIO(b"DOCX-DUMMY")
        resp = self.client.get('/api/v1/certificado/1/docx')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.wordprocessingml.document', resp.headers.get('Content-Type', ''))
        self.assertIn('attachment', resp.headers.get('Content-Disposition', ''))


if __name__ == '__main__':
    unittest.main()
