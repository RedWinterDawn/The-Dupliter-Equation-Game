class Dupliter < Formula
  desc "Retro BBS-style terminal simulator for the Dupliter gravitational temporal anchor hypothesis"
  homepage "https://github.com/RedWinterDawn/The-Dupliter-Equation-Game"
  url "https://raw.githubusercontent.com/RedWinterDawn/The-Dupliter-Equation-Game/r2d2/dupliter_bbs.py"
  sha256 "fb87384baacf2aea65eeef29f459a9279e54459183bc553e9d96342f7bd3dd20"
  license "MIT"

  depends_on "python@3.11"

  def install
    bin.install "dupliter_bbs.py" => "dupliter"
  end

  test do
    assert_predicate bin/"dupliter", :exist?
  end
end
