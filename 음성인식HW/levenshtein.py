# import numpy


class Levenshtein(object):

    def __init__(self):
        super(Levenshtein, self).__init__()

    @staticmethod
    def editDistance(ref, stt):
        """
        Levenshtein Distance 구현

        :param ref: reference (정답 텍스트, 기준)
        :param stt: STT result (인식결과 텍스트)
        :return: Levenshtein Distance Matrix (len(ref) * len(stt))
        """

        # edited --------------------------------------
        # 기존 방법
        # d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint32).reshape((len(r) + 1, len(h) + 1))

        # numpy 패키지 안쓰고 파이썬으로만 짜는 방법
        distance_matrix = [[0 for y in range(len(stt)+1)] for x in range(len(ref)+1)]
        # -------------------------------------------

        # 초기값 설정 
        for x in range(len(ref) + 1):       # x축: 정답지, i
            for y in range(len(stt) + 1):   # y축: 인식결과, j
                if x == 0:
                    distance_matrix[0][y] = y
                elif y == 0:
                    distance_matrix[x][0] = x

        # 글자가 서로 동일하면 대각선 값을 가져온다
        # 변경이 필요하면 대각선 값에서 + 1을 한다.
        # 삽입이 필요하면 위의 값에서 +1을 한다.
        # 삭제가 필요하면 왼쪽 값에서 +1을 한다.
        # 1~4의 경우에서 최소값을 가져온다.

        for x in range(1, len(ref) + 1):
            for y in range(1, len(stt) + 1):
                #print(ref[x - 1])
                if ref[x - 1] == stt[y - 1]:
                    distance_matrix[x][y] = distance_matrix[x - 1][y - 1]
                else:
                    substitute = distance_matrix[x - 1][y - 1] + 1
                    insert = distance_matrix[x][y - 1] + 1
                    delete = distance_matrix[x - 1][y] + 1
                    distance_matrix[x][y] = min(substitute, insert, delete)

        return distance_matrix

    @staticmethod
    def getStepList(ref, stt, d):
        """
        TOT, MAT, INS, DEL, SUB 리스트 출력 함수

        :param ref: Reference
        :param stt: STT result
        :param d: Levenshtein Distance Matrix
        :return:  Matched info list
        """

        x = len(ref)
        y = len(stt)

        list = []

        while True:
            if x == 0 and y == 0:
                break
            elif d[x][y] == d[x-1][y-1] and ref[x-1] == stt[y-1] and x >= 1 and y >= 1:
                list.append("m")
                x = x - 1
                y = y - 1
            elif d[x][y] == d[x][y - 1] + 1 and y >= 1:
                list.append("i")
                x = x
                y = y - 1
            elif d[x][y] == d[x - 1][y - 1] + 1 and x >= 1 and y >= 1:
                list.append("s")
                x = x - 1
                y = y - 1
            else:
                list.append("d")
                x = x - 1
                y = y

        return list[::-1]   # 역으로 변경


def cer(info):

    ref_sent = info.get('ref')
    stt_sent = info.get('hyp')

    ref = list(''.join(ref_sent.split()))
    stt = list(''.join(stt_sent.split()))

    levenshtein = Levenshtein()

    distance_matrix = levenshtein.editDistance(ref, stt)

    if len(ref) != 0:
        cer_rate = float(distance_matrix[len(ref)][len(stt)]) / len(ref) * 100
    else:
        cer_rate = float('inf')

    result_list = levenshtein.getStepList(ref, stt, distance_matrix)

    # 레퍼런스(정답지)의 글자 수 
    num_total = len(ref)

    #/*
    #m_list = list()
    #for item in match_list:
    #    if item == 'm':
    #        m_list.append(item)
    #
    #num_mat = len(m_list)

    num_mat = len([item for item in result_list if item == 'm'])
    num_sub = len([item for item in result_list if item == 's'])
    num_del = len([item for item in result_list if item == 'd'])
    num_ins = len([item for item in result_list if item == 'i'])

    cer_info = {'cer': cer_rate, 'tot': num_total,
                'mat': num_mat, 'sub': num_sub,
                'del': num_del, 'ins': num_ins,
                'list': result_list}

    return cer_info





if __name__ == '__main__':

    ref_text = '안녕하세요 만나서 반감'  # 전사 결과 (에러3개, 오, 서, 감)
    stt_text = '안녕하세요오 만나 반갑'  # STT 결과

    sentence_info = {'ref': ref_text, 'hyp': stt_text}
    cer_info = cer(sentence_info)

    print('refer : %s' % ref_text)
    print('hyper : %s' % stt_text)
    print('match list : ', cer_info.get('list'))

    # Edit --------------------------------------
    cer_rate = 100 - cer_info.get('cer')
    print('cer : %f' % cer_rate if cer_rate > 0 else 0.0)  # 인식률 (Character Error Rate)
    # -------------------------------------------

    print('tot : %d' % cer_info.get('tot'))  # 전체 음절 수
    print('mat : %d' % cer_info.get('mat'))  # 매치 음절 수
    print('sub : %d' % cer_info.get('sub'))  # 교체 에러 수
    print('ins : %d' % cer_info.get('ins'))  # 삽입 에러 수
    print('del : %d' % cer_info.get('del'))  # 삭제 에러 수
