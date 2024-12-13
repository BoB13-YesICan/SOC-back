# desc: 짧은 설명
#"desc": "000으로 들어온 DoS공격입니다. ",

#[공격 유형, 사유]
#detailed: 긴 설명
# 공격의 기술적 설명: 어떤 방식으로 이루어졌는가.
# 공격의 영향: 시스템에 어떤 문제가 발생했는가.
# 공격 탐지 방법: 어떤 데이터를 통해 탐지했는가.
# 공격 사례: 유사 사례 또는 실험적 사례.
# 방어 및 완화 방법: 구체적 조치 제안.
# 참고 자료: 논문, 연구 링크 제공.
ids = {
    0: {
        "type": "normal",
        "desc": "normal_packet",
        "detailed":"normal",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    1: {
        "type": "DoS",
        "desc": "CAN ID XXX으로 들어온 DoS공격입니다. ",
        "detailed": "같은 CAN ID에 대해서 동일한 페이로드를 5ms 이내로 여러번 주입하였습니다. CAN버스 과부하로 인한 통신 속도 저하 및 패킷 로스가 발생합니다. 같은 CAN ID에 대해서 5ms이내로 들어왔으며, DBC에 정의되지 않은 CAN ID, DLC 혹은 Payload를 가진 packet이 들어왔으며, CAN ID가 동일한 이전 패킷과의 Payload가 일치하여 DoS로 판단되었습니다. 해당 CAN ID로 들어오는 패킷을 차단하십시오.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    2: {
        "type": "DoS",
        "desc": "CAN ID XXX으로 들어온 DoS공격입니다. ",
        "detailed": "같은 CAN ID에 대해서 동일한 페이로드를 5ms 이내로 여러번 주입하였습니다. CAN버스 과부하로 인한 통신 속도 저하 및 패킷 로스가 발생합니다. CAN ID XXX의 정보가 덮어씌워집니다. 같은 CAN ID에 대해서 5ms이내로 들어왔으며, DBC에 정의되는 CAN ID, DLC 혹은 Payload를 가진 packet이 들어왔으며, CAN ID가 동일한 이전 패킷과의 Payload가 일치하여 DoS로 판단되었습니다. DoS공격이 발생하는 파티션을 다른 파티션과 분리하십시오.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    3: {
        "type": "DoS",
        "desc": "CAN ID XXX으로 들어온 DoS공격입니다. ",
        "detailed": "같은 CAN ID에 대해서 동일한 Payload를 비주기적으로 주입하였습니다. CAN ID XXX의 정보가 덮어씌워집니다. DBC에 정의된 CAN ID, DLC 혹은 Payload를 가진 packet이 들어왔으며, CAN ID가 동일한 이전 패킷과의 Payload가 일치하여 DoS로 판단되었습니다. DoS공격이 발생하는 파티션을 다른 파티션과 분리하십시오.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    4: {
        "type": "Fuzzing",
        "desc": "CAN ID XXX으로 들어온 fuzzing공격입니다. ",
        "detailed": "CAN ID에 대해서 서로 다른 페이로드를 Xms간격으로 주입하였습니다. CAN버스 과부하로 인한 통신 속도 저하 및 패킷 로스가 발생합니다. CAN ID XXX의 정보가 덮어씌워집니다. 차량에서 발생하는 현상들을 통해 공격자가 해당 CAN ID와 페이로드가 어떤 기능을 하는지 유추 할 수 있습니다. DBC에 정의되지 않은 CAN ID, DLC 혹은 Payload를 가진 packet이 들어와서 Fuzzing으로 판단되었습니다. DBC에 정의되지 않은 CAN ID로 들어오는 패킷들을 차단하십시오.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    5: {
        "type": "Fuzzing",
        "desc": "CAN ID XXX으로 들어온 fuzzing공격입니다. ",
        "detailed": "CAN ID에 대해서 서로 다른 페이로드를 Xms간격으로 주입하였습니다. CAN버스 과부하로 인한 통신 속도 저하 및 패킷 로스가 발생합니다. CAN ID XXX의 정보가 덮어씌워집니다. 차량에서 발생하는 현상들을 통해 공격자가 해당 CAN ID와 페이로드가 어떤 기능을 하는지 유추 할 수 있습니다. 해당 CAN ID의 평균 유사도는 XX퍼센트인데 해당 패킷과 이전 패킷과의 유사도가 XX퍼센트이어서 악성으로 탐지하였습니다. DoS공격이 발생하는 파티션을 다른 파티션과 분리하십시오.",
        "c": ["can_id","similarity"],
        "img":"./asset/1.png"
    },
    6: {
        "type": "Replay",
        "desc": "CAN ID XXX, payload XXX으로 들어온 replay공격입니다. ",
        "detailed": "CAN ID에 대해서 동일한 패킷을 비주기적, 반복적으로 주입하였습니다. 공격자가 의도한 행동을 차량이 반복하여 수행합니다. CAN ID 000에 대해서 XXXX의 동일한 페이로드가 비주기적, 반복적으로 탐지되어 악성으로 탐지하였습니다. 공격 패킷을 주입하고 있는 디바이스를 제거하십시오.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    7: {
        "type": "Suspension",
        "desc": "XXX으로 들어온 UDS 리셋 공격입니다. ",
        "detailed": "CAN ID 7XX에 대해서 요청 SID(ServiceID) 0x11 빠르게 보내어 응답 SID 0x51, 즉 ECU reset을 반복적으로 수행하였습니다. 반복적인 ECU reset으로 인하여 해당 ECU가 패킷을 정상적으로 송수신 할 수 없습니다.  이 증상은 공격이 끝나거나 차량을 재시동하기 전까지 반복됩니다. 요청 SID 0x11 보내고 응답 SID 0x51을 받는 작업을 1초 이내의 간격으로 반복적으로 수행하여 악성으로 탐지하였습니다. 공격 패킷을 주입하고 있는 디바이스를 제거하거나 차량을 재시동하여 ECU를 재기동시키십시오.",
        "c": ["can_id","reset_count"],
        "img":"./asset/1.png"
    },
    8: {
        "type": "Suspension",
        "desc": "CAN ID XXX으로 들어온 suspension공격입니다. ",
        "detailed": "공격자가 CAN ID XXX를 발생시키는 ECU를 마비시켰습니다. CAN ID XXX를 발생시키는 ECU가 정상 작동하지 못해 차량의 특정 동작이 지연되거나 마비됩니다. CAN ID 000에 대해서 패킷이 기존 주기의 5배 +3초보다 늦게 들어와 악성으로 탐지하였습니다. 공격 패킷을 주입하고 있는 디바이스를 제거하거나 차량을 재시동하여 ECU를 재기동시키십시오.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./asset/1.png"
    },
    9: {
        "type": "Masquerade",
        "desc": "CAN ID 000으로 들어온 masquerade입니다. ",
        "detailed": "CAN ID XXX를 전송하는 ECU를 정지시키고 공격자가 패킷을 주입하고 있습니다. 차량이 운전자의 특정 동작에 반응하지 못하거나, 차량이 공격자가 의도한 동작을 수행하게 됩니다. Clockskew가 기존 패킷들과 일치하지 않아 악성으로 탐지하였습니다. 공격 패킷을 주입하고 있는 디바이스를 제거하거나, 차량을 재시동하여 ECU를 재기동시키십시오.",
        "c": ["can_id","clock_skew", "clock_skew_min", "clock_skew_max"],
        "img":"./asset/1.png"
    }
}
