#[공격 유형, 사유]
#detailed: 
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
        "img":"./report/asset/ruleset.png"
    },
    1: {
        "type": "DoS",
        "desc": "dbc_dos_packet",
        "detailed": "ID 000으로 패킷이 들어왔습니다. 이 경우, 모든 CAN 패킷들이 지연됩니다.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./report/asset/ruleset.png"
    },
    2: {
        "type": "DoS",
        "desc": "time_dos_packet",
        "detailed": "0.0004?초 이내로 패킷이 대량 주입되었습니다. 이 경우, 주입된 패킷 ID 보다 우선순위가 낮은 CAN 패킷들이 지연됩니다. 0.0004?초 이내로 패킷이 대량 주입되었습니다. 이 경우, 주입된 패킷 ID 보다 우선순위가 낮은 CAN 패킷들이 지연됩니다. 0.0004?초 이내로 패킷이 대량 주입되었습니다. 이 경우, 주입된 패킷 ID 보다 우선순위가 낮은 CAN 패킷들이 지연됩니다. 0.0004?초 이내로 패킷이 대량 주입되었습니다. 이 경우, 주입된 패킷 ID 보다 우선순위가 낮은 CAN 패킷들이 지연됩니다.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./report/asset/ruleset.png"
    },
    3: {
        "type": "DoS",
        "desc": "payload_dos_packet",
        "detailed": "payload가 같은 패킷이 짧은 시간 동안 대량 주입되었습니다. DoS의 가능성이 있습니다. payload가 같은 패킷이 짧은 시간 동안 대량 주입되었습니다. DoS의 가능성이 있습니다. payload가 같은 패킷이 짧은 시간 동안 대량 주입되었습니다. DoS의 가능성이 있습니다. payload가 같은 패킷이 짧은 시간 동안 대량 주입되었습니다. DoS의 가능성이 있습니다. payload가 같은 패킷이 짧은 시간 동안 대량 주입되었습니다. DoS의 가능성이 있습니다.payload가 같은 패킷이 짧은 시간 동안 대량 주입되었습니다. DoS의 가능성이 있습니다.",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./report/asset/ruleset.png"
    },
    4: {
        "type": "Fuzzing",
        "desc": "dbc_fuzzing_packet",
        "detailed": """
        0.0004초 이내로 패킷이 대량 주입되었습니다. 이 공격은 네트워크의 대역폭을 소진하여 우선순위가 낮은 CAN 패킷(ID: 0x123, 0x456)의 지연을 초래하였습니다. 
탐지는 주입된 패킷 간격(`time_diff`)이 0.0004초 이하로 짧은 주기를 가지는 것을 통해 이루어졌습니다. 
본 공격은 2023년 X 차량 모델의 네트워크에서 유사한 패턴으로 재현된 사례가 있습니다. 
이러한 공격은 `rate-limiting`을 적용하고, CAN ID 0x789의 비정상적인 사용 패턴을 모니터링하여 방어할 수 있습니다.
""",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./report/asset/ruleset.png"
    },
    5: {
        "type": "Fuzzing",
        "desc": "similarity_fuzzing_packet",
        "detailed": """
        0.0004초 이내로 패킷이 대량 주입되었습니다. 이 공격은 네트워크의 대역폭을 소진하여 우선순위가 낮은 CAN 패킷(ID: 0x123, 0x456)의 지연을 초래하였습니다. 
탐지는 주입된 패킷 간격(`time_diff`)이 0.0004초 이하로 짧은 주기를 가지는 것을 통해 이루어졌습니다. 
본 공격은 2023년 X 차량 모델의 네트워크에서 유사한 패턴으로 재현된 사례가 있습니다. 
이러한 공격은 `rate-limiting`을 적용하고, CAN ID 0x789의 비정상적인 사용 패턴을 모니터링하여 방어할 수 있습니다.
""",
        "c": ["can_id","similarity"],
        "img":"./report/asset/ruleset.png"
    },
    6: {
        "type": "Replay",
        "desc": "replay_packet",
        "detailed": """
        0.0004초 이내로 패킷이 대량 주입되었습니다. 이 공격은 네트워크의 대역폭을 소진하여 우선순위가 낮은 CAN 패킷(ID: 0x123, 0x456)의 지연을 초래하였습니다. 
탐지는 주입된 패킷 간격(`time_diff`)이 0.0004초 이하로 짧은 주기를 가지는 것을 통해 이루어졌습니다. 
본 공격은 2023년 X 차량 모델의 네트워크에서 유사한 패턴으로 재현된 사례가 있습니다. 
이러한 공격은 `rate-limiting`을 적용하고, CAN ID 0x789의 비정상적인 사용 패턴을 모니터링하여 방어할 수 있습니다.
""",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./report/asset/ruleset.png"
    },
    7: {
        "type": "Suspension",
        "desc": "uds_suspension_packet",
        "detailed": "UDS를 통한 패킷이 주입되었습니다. ",
        "c": ["can_id","reset_count"],
        "img":"./report/asset/ruleset.png"
    },
    8: {
        "type": "Suspension",
        "desc": "time_suspension_packet",
        "detailed": """
        0.0004초 이내로 패킷이 대량 주입되었습니다. 이 공격은 네트워크의 대역폭을 소진하여 우선순위가 낮은 CAN 패킷(ID: 0x123, 0x456)의 지연을 초래하였습니다. 
탐지는 주입된 패킷 간격(`time_diff`)이 0.0004초 이하로 짧은 주기를 가지는 것을 통해 이루어졌습니다. 
본 공격은 2023년 X 차량 모델의 네트워크에서 유사한 패턴으로 재현된 사례가 있습니다. 
이러한 공격은 `rate-limiting`을 적용하고, CAN ID 0x789의 비정상적인 사용 패턴을 모니터링하여 방어할 수 있습니다.
""",
        "c": ["can_id","time_diff", "periodic"],
        "img":"./report/asset/ruleset.png"
    },
    9: {
        "type": "Masquerade",
        "desc": "clock_skew",
        "detailed": """
        0.0004초 이내로 패킷이 대량 주입되었습니다. 이 공격은 네트워크의 대역폭을 소진하여 우선순위가 낮은 CAN 패킷(ID: 0x123, 0x456)의 지연을 초래하였습니다. 
탐지는 주입된 패킷 간격(`time_diff`)이 0.0004초 이하로 짧은 주기를 가지는 것을 통해 이루어졌습니다. 
본 공격은 2023년 X 차량 모델의 네트워크에서 유사한 패턴으로 재현된 사례가 있습니다. 
이러한 공격은 `rate-limiting`을 적용하고, CAN ID 0x789의 비정상적인 사용 패턴을 모니터링하여 방어할 수 있습니다.
""",
        "c": ["can_id","clock_skew", "clock_skew_min", "clock_skew_max"],
        "img":"./report/asset/ruleset.png"
    }
}
