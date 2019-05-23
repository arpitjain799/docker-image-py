import unittest

from docker_image import digest
from docker_image import reference


class TestReference(unittest.TestCase):
    def test_reference(self):
        def create_test_case(input_, err=None, repository=None, hostname=None, tag=None, digest=None):
            return {
                'input': input_,
                'err': err,
                'repository': repository,
                'hostname': hostname,
                'tag': tag,
                'digest': digest,
            }

        test_cases = [
            create_test_case(input_='test_com', repository='test_com'),
            create_test_case(input_='test.com:tag', repository='test.com', tag='tag'),
            create_test_case(input_='test.com:5000', repository='test.com', tag='5000'),
            create_test_case(input_='test.com/repo:tag', repository='test.com/repo', hostname='test.com', tag='tag'),
            create_test_case(input_='test:5000/repo', repository='test:5000/repo', hostname='test:5000'),
            create_test_case(input_='test:5000/repo:tag', repository='test:5000/repo', hostname='test:5000', tag='tag'),
            create_test_case(input_='test:5000/repo@sha256:{}'.format('f' * 64),
                             repository='test:5000/repo', hostname='test:5000', digest='sha256:{}'.format('f' * 64)),
            create_test_case(input_='test:5000/repo:tag@sha256:{}'.format('f' * 64),
                             repository='test:5000/repo', hostname='test:5000', tag='tag', digest='sha256:{}'.format('f' * 64)),
            create_test_case(input_='test:5000/repo', repository='test:5000/repo', hostname='test:5000'),
            create_test_case(input_='', err=reference.NameEmpty),
            create_test_case(input_=':justtag', err=reference.ReferenceInvalidFormat),
            create_test_case(input_='@sha256:{}'.format('f' * 64), err=reference.ReferenceInvalidFormat),
            create_test_case(input_='repo@sha256:{}'.format('f' * 34), err=digest.DigestInvalidLength),
            create_test_case(input_='validname@invaliddigest:{}'.format('f' * 64), err=digest.DigestUnsupported),
            create_test_case(input_='{}a:tag'.format('a/' * 128), err=reference.NameTooLong),
            create_test_case(input_='{}a:tag-puts-this-over-max'.format('a/' * 127), repository='{}a'.format('a/' * 127),
                             hostname='a', tag='tag-puts-this-over-max'),
            create_test_case(input_='aa/asdf$$^/aa', err=reference.ReferenceInvalidFormat),
            create_test_case(input_='sub-dom1.foo.com/bar/baz/quux', repository='sub-dom1.foo.com/bar/baz/quux',
                             hostname='sub-dom1.foo.com'),
            create_test_case(input_='sub-dom1.foo.com/bar/baz/quux:some-long-tag', repository='sub-dom1.foo.com/bar/baz/quux',
                             hostname='sub-dom1.foo.com', tag='some-long-tag'),
            create_test_case(input_='b.gcr.io/test.example.com/my-app:test.example.com',
                             repository='b.gcr.io/test.example.com/my-app', hostname='b.gcr.io', tag='test.example.com'),
            create_test_case(input_='xn--n3h.com/myimage:xn--n3h.com', repository='xn--n3h.com/myimage', hostname='xn--n3h.com',
                             tag='xn--n3h.com'),
            create_test_case(input_='xn--7o8h.com/myimage:xn--7o8h.com@sha512:{}'.format('f' * 128),
                             repository='xn--7o8h.com/myimage', hostname='xn--7o8h.com', tag='xn--7o8h.com',
                             digest='sha512:{}'.format('f' * 128)),
            create_test_case(input_='foo_bar.com:8080', repository='foo_bar.com', tag='8080'),
            create_test_case(input_='foo/foo_bar.com:8080', repository='foo/foo_bar.com', hostname='foo', tag='8080'),
            create_test_case(input_='123.dkr.ecr.eu-west-1.amazonaws.com:lol/abc:d', err=reference.ReferenceInvalidFormat),
        ]

        for tc in test_cases:
            if tc['err']:
                self.assertRaises(tc['err'], reference.Reference.parse, tc['input'])
                continue

            try:
                r = reference.Reference.parse(tc['input'])
            except Exception as e:
                raise e
            else:
                if tc['repository']:
                    self.assertEqual(tc['repository'], r['name'])

                if tc['hostname']:
                    hostname, _ = r.split_hostname()
                    self.assertEqual(tc['hostname'], hostname)

                if tc['tag']:
                    self.assertEqual(tc['tag'], r['tag'])

                if tc['digest']:
                    self.assertEqual(tc['digest'], r['digest'])
