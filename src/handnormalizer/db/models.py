from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey
from typing import List, Optional

Base = declarative_base()

class Hand(Base):

    __tablename__= "hands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    site: Mapped[str] = mapped_column(String, index=True)
    site_hand_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    hero_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_maximum_raise_2bet: Mapped[bool] = mapped_column(Boolean, index=True)

    player_stats: Mapped[List["PlayerHandStat"]] = relationship(
        "PlayerHandStat", back_populates="hand", cascade="all, delete-orphan"
    )


class PlayerHandStat(Base):
    __tablename__ = "player_hand_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hand_id: Mapped[int] = mapped_column(ForeignKey("hands.id"), index=True)
    player_name: Mapped[str] = mapped_column(String, index=True)

    #Temp
    bet_flop_any: Mapped[bool] = mapped_column(Boolean, index=True)
    checked_flop: Mapped[bool] = mapped_column(Boolean, index=True)
    folded_flop_any: Mapped[bool] = mapped_column(Boolean, index=True)

    hand: Mapped["Hand"] = relationship("Hand", back_populates="player_stats")


def init_db(engine):
    Base.metadata.create_all(bind=engine)



